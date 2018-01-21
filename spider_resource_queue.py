#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the spider taskqueue module, which records and manages the task order

Authors: Wan Li
Date:    2015/09/02
"""

import threading
import Queue
import os
import logging

class Resource(object):
    """Spider resource class

    Resources are objects stores necessary infomation for the spider task program.

    Attributes:
        url: page url
        level: tree level from root node
    """
    
    def __init__(self, url, level, queue):
        """Resource initializer 

        Initializes resource object with configurations

        Args:
            url: Number of threads to run in parallel
            level: The level of current node on the parse tree
            queue: Resource queue on which actions done
        """
        self.url = url
        self.level = level
        self.queue = queue

    def __str__(self):
        return "<level:{}, url:{}>".format(self.level, self.url)


class ResourceQueue(object):
    """Spider resource queue class.

    Hold resources spider engine is to perform tasks on

    Attributes:
        resources: an array holding resources of actions to be performed
    """

    def __init__(self):
        self.resource_queue = Queue.Queue()
        self.lock = threading.Lock()
        self.lookup_hash_set = set()

    def __check_exist(self, url):
        hash_int = hash(url)
        if hash_int in self.lookup_hash_set:
            return True
        else:
            self.lookup_hash_set.add(hash_int)
            return False

    def add_from_file(self, file_path):
        """Parse urls.

        Parse urls from file and adds to queue.

        Args:
            file: Url file path.

        Returns: True if success, otherwise False
        """

        #Validate file path
        if not os.path.isfile(file_path):
            err_msg = "Error: config file not exists. (%s)" % file_path
            logging.error(err_msg)
            return False
        try:
            with open(file_path) as urls:
                for url in urls:
                    if len(url.strip(' ')) < 1:
                        continue
                    self.put(Resource(url, 0, self))
        except Exception as err:
            logging.error("ERROR: url file malformed. (%s) ." % err)
            return False
        return True

    def put(self, resource):
        """Put a resource into the queue"""
        self.lock.acquire()
        if not self.__check_exist(resource.url):
            self.resource_queue.put(resource)
        self.lock.release()

    def get(self):
        """Dequeue a resource from the queue and return it."""
        self.lock.acquire()
        queue_elem = None
        try:
            if not self.resource_queue.empty():
                queue_elem = self.resource_queue.get(block = True, timeout = 10.0)
        except Exception as err:
            logging.error("ERROR: failed to get resource. (%s) ." % err)
            pass
        self.lock.release()
        return queue_elem

    def task_done(self):
        """Forward invocation."""
        self.resource_queue.task_done()

    def join(self):
        """Forward invocation."""
        self.resource_queue.join()
