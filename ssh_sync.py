#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import config
import os
import subprocess

class SshSync:
    
    def __init__(self, host, keypath):
        self.keypath = keypath
        self.host = host

    def __exec(self, cmd, verbose=False):
        args = " ".join(cmd)
        if verbose:
            print args

        result = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE).communicate()[0]

        if verbose:
            print result
        return result

    def sync(self, source_path, dest_path):
        ssh = "'ssh -i "+self.keypath+"'"
        dest = self.host + ":" + dest_path
        cmd = ["rsync", "-e", ssh, "-avrz", "--delete", source_path, dest, ]
        self.__exec(cmd, verbose=True)


if __name__ == '__main__':
    scriptdir = os.path.dirname(__file__)
    os.chdir(scriptdir)

    conf = config.Config()
    hosts =         conf.parser.get("sync","hosts").split(",")
    keyfilepath =   conf.parser.get("sync","keyfilepath")
    source =        conf.parser.get("sync","source")
    dest =          conf.parser.get("sync","dest")

    for host in hosts:
        sshsync = SshSync(host, keyfilepath)
        sshsync.sync(source, dest)
