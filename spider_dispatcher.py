#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the spider dispatcher module, which manages the taks concurrency

Authors: Wan Li
Date:    2015/09/02
"""

import threading
import logging

class SpiderDispatcher(object):
    """Spider dispatcher class.

    This class controls the threading and concurrency

    Attributes:
        num_threads: concurrency
        resource_queue: object queue on which task is performed
        handler: task performer object
    """

    def __init__(self, num_threads, resource_queue):
        """Dispatcher initializer 

        Initializes dispatcher with configurations

        Args:
            num_threads: Number of threads to run in parallel
            resource_queue: Resource queue on which actions done
        """
        
        self.num_threads = num_threads
        self.queue = resource_queue
        self.handler = None

    def __do_work(self, task_obj):
        """Perform action on task object."""
        self.handler(task_obj)

    def __worker(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            try:
                self.__do_work(item)
            except Exception as e:
                logging.error("ERROR:{}".format(e))
                break
            self.queue.task_done()

    def setup_dispatch_handler(self, handler):
        """Setup referred data handler."""
        self.handler = handler

    def start_dispatch(self):
        """Start tasks."""

        #Start working
        if self.num_threads > 1:
            for thread_idx in xrange(self.num_threads):
                worker = threading.Thread(target=self.__worker)
                worker.daemon = True
                worker.start()
        else:
            self.__worker()

        #Wait until all tasks done
        self.queue.join()
        logging.info("Dispatch done.")
