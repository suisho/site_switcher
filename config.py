#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

class Config:
    def __init__(self, conf_file="config.ini"):
        parser = ConfigParser.SafeConfigParser()
        parser.read(conf_file)
        self.parser = parser

        #self.debug = config.get("debug","debug")
        self.debug = False

        # site_switcher.py
        self.packages = parser.get("path", "packages")
        self.production = parser.get("path", "production")
        self.staging = parser.get("path", "staging")
        self.www = parser.get("path", "www")
        