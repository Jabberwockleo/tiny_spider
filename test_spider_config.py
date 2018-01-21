#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the unit test module for spider_config

Authors: Wan Li
Date:    2015/09/02
"""

import unittest

import spider_config

class TestSpiderConfig(unittest.TestCase):
    """Unit Test Class For SpiderConfig"""
    
    def setUp(self):
        pass
        
    def test_parse(self):
        """Test parse from file."""
        config = spider_config.SpiderConfig()
        config.parse("../spider.conf")
        self.assertEqual(config.get_config("url_list_file"), "urls.conf")
        
    def test_set_get(self):
        """Test setter and getter"""
        config = spider_config.SpiderConfig()
        config.set_config("key", "val")
        val = config.get_config("key")
        self.assertEqual(val, "val")

if __name__ == "__main__":
    unittest.main()
