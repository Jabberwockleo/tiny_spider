#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the config manager module

Authors: Wan Li
Date:    2015/09/02
"""

import os.path
import ConfigParser
import logging

class SpiderConfig(object):
    """Spider config class.

    Parse config file and load into dict.

    Attributes:
        config_dict: the config to store spider configuration loaded from file
    """

    def __init__(self):
        self.config_dict = {}

    def __parse_key(self, parser, key):
        """Parse value for key from config file

        Parses retrieve a value for key from config file.

        Args:
            parser: Config parser
            key: The key for which value to be retrieved

        Returns: value for key, None if not exists
        """
        
        return parser.get("spider", key)

    def parse(self, file_path):
        """Parse config dict from file

        Parses config and loads in a dict.

        Args:
            file: Config file path.

        Returns: True if success, otherwise False
        """

        #Validate file path
        if not os.path.isfile(file_path):
            err_msg = "Error: config file not exists. (%s)" % file_path
            logging.error(err_msg)
            return False

        #Parse config file
        conf_parser = ConfigParser.ConfigParser()
        try:
            conf_parser.read(file_path)
        except Exception as err:
            err_msg = "Error: config file malformed. (%s)" % err
            logging.error(err_msg)
            return False

        #Load config into dict
        try:
            key_list = ["url_list_file", "output_directory", "max_depth",
                        "crawl_interval", "crawl_timeout", "target_url",
                        "thread_count"]
            for key in key_list:
                self.set_config(key, self.__parse_key(conf_parser, key))
        except Exception as err:
            err_msg = "Error: config file format error. (%s)" % err
            logging.error(err_msg)
            return False

        return True

    def set_config(self, key, val):
        """Assign config val
        Args:
            key: config key to be set
            val: config value to be stored
        """

        self.config_dict[key] = val

    def get_config(self, key):
        """Retrieve config val
        Args:
            key: config key to be query
        Returns: value for key or None if key is not set
        """

        return self.config_dict.get(key, None)
