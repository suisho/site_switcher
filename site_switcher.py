#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import logging
import subprocess

import sys

import config

logger = logging.getLogger()
#logger.level = logging.DEBUG


class PackageDirectory:
    def __init__(self, base_dir, name):
        self.path = base_dir + "/" + name
        self.time = self.parse_dir_time(name)

    def __str__(self):
        return "(" + str(self.time) + ")" + self.path

    @staticmethod
    # 配列にアクセスしてダメだったらデフォルト値返す
    def getbyint(array, index, defalt=0):
        try:
            return int(array[index])
        except Exception:
            return defalt

    @staticmethod
    # ディレクトリから時間を返す
    def parse_dir_time(dir_name):
        self = PackageDirectory
        time_split = dir_name.split("_")
        dirTime = datetime.datetime(PackageDirectory.getbyint(time_split, 0, 1990),
                                    PackageDirectory.getbyint(time_split, 1, 1),
                                    PackageDirectory.getbyint(time_split, 2, 1),
                                    PackageDirectory.getbyint(time_split, 3, 0),
                                    PackageDirectory.getbyint(time_split, 4, 0))
        return dirTime

    #ディレクトリの指定期間のものを返す
    @staticmethod
    def get_span_dir_list(directory, start, end):
        staging_dirs = os.listdir(directory)
        dirs = []
        for _dir in staging_dirs:
            try:
                staging_dir = PackageDirectory(directory, _dir)
                logging.debug([str(start), str(staging_dir.time), str(end)])
                if start <= staging_dir.time <= end:
                    dirs.append(staging_dir)
            except Exception:  # todo ちゃんとエラーハンドリング
                pass
        return dirs


class SiteSwitcher:
    def __init__(self, target_dir, packages_dir):
        self.target_dir = target_dir
        self.packages_dir = packages_dir

    #現在時刻取得
    def get_now(self):
        # TODO:タイムゾーン
        time = datetime.datetime.now()
        return time

    def get_target_time(self):
        link = self.readlink(self.target_dir + "/htdocs")
        basename = os.path.basename(link)
        return  PackageDirectory.parse_dir_time(basename)

    # timeを元に
    def switch_auto(self, time=None):
        #現在の本番dirの時刻取得
        production_time = self.get_target_time()

        if time is None:
            time = self.get_now()
        #productionより後で指定時刻より前
        dirs = PackageDirectory.get_span_dir_list(self.packages_dir,
                                                  start=production_time,
                                                  end=time)
        if len(dirs) == 0:
            print "No packages target"
            return

        #時間でソートして一番ケツに来るのがスイッチ対象
        cmp_by_time = lambda a, b: cmp(a.time, b.time)
        dirs.sort(cmp=cmp_by_time)
        link_target = self.target_dir+"/htdocs"
        self.exec_ln(dirs.pop().path, link_target)
        print self.readlink(link_target)

    def exec_command(self, cmd):
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        logging.debug([cmd, result])
        return result
        #return result[1]

    #ln コマンドを行う
    def exec_ln(self, target, link_name):
        # シンボリックリンク、強制、シンボリックリンクならファイルとして扱う、verbose
        cmd = ["ln", "-sfnv", target, link_name]
        return self.exec_command(cmd)

    def readlink(self, target):
        cmd = ["readlink", target]
        return self.exec_command(cmd)


def swich_production():
    conf = config.Config()
    projects = os.listdir(conf.packages)
    for project in projects:
        print "switch:" + project
        prod_dir = conf.production + "/" + project
        packages_dir = conf.packages + "/" + project
        switcher = SiteSwitcher(prod_dir, packages_dir)
        switcher.switch_auto()

if __name__ == '__main__':
    scriptdir = os.path.dirname(__file__)
    os.chdir(scriptdir)
    #argparser = argparse.ArgumentParser();
    #argparser.add_argument('-s',dest='staging_time')
    swich_production()
