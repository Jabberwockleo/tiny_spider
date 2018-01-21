#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the unit test module for spider_dispatcher

Authors: Wan Li
Date:    2015/09/02
"""

import unittest
import Queue
import threading

import spider_dispatcher
import spider_resource_queue

global_test_sum = 0

class TestSpiderDispatcher(unittest.TestCase):
    """Unit Test Class For SpiderDispatcher"""

    def setUp(self):
        queue = Queue.Queue()
        for data_idx in xrange(10):
            queue.put(data_idx)
        self.dispatcher = spider_dispatcher.SpiderDispatcher(3, queue)

    def test_setup_dispatch_handler(self):
        """Test setter of dispatcher handler."""
        def test_handler(obj):
            """Provided handler."""
            return "test"
        self.dispatcher.setup_dispatch_handler(test_handler)
        ret_handler = self.dispatcher.handler
        self.assertEqual(ret_handler(None), "test")

    def test_start_dispatch(self):
        """Test dispatcher main process."""
        lock = threading.Lock()
        def handler(val):
            """Provided handler."""
            lock.acquire()
            global global_test_sum
            global_test_sum += val
            lock.release()
        self.dispatcher.setup_dispatch_handler(handler)
        self.dispatcher.start_dispatch()
        self.assertEqual(global_test_sum, 45)


if __name__ == "__main__":
    unittest.main()
