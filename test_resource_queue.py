#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the unit test module for spider_resource_queue

Authors: Wan Li
Date:    2015/09/02
"""

import unittest

import spider_resource_queue

class TestResourceQueue(unittest.TestCase):
    """Unit Test Class For ResourceQueue"""
    
    def setUp(self):
        pass
        
    def test_put_get(self):
        """Test queue set and get operations."""
        self.queue = spider_resource_queue.ResourceQueue()
        self.queue.put(spider_resource_queue.Resource("test", 0, self.queue))
        val = self.queue.get()
        self.assertEqual(val.url, "test")
        self.assertEqual(val.level, 0)
        
if __name__ == "__main__":
    unittest.main()
