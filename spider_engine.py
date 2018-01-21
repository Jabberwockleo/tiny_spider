#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the spider engine module, which is the controller of spider actions

Authors: Wan Li
Date:    2015/09/02
"""

import time
import re
import logging

from bs4 import BeautifulSoup

import spider_utilities as util
import spider_config
import spider_dispatcher
import spider_resource_queue

class SpiderEngine(object):
    """Spider engine class.

    Centralized controller of spider behaviour

    Attributes:
        spider_config: the config to store spider configuration loaded from file
        spider_dispatcher: the threading controller to perform tasks
        spider_queue: the
    """

    def __init__(self, config, dispatcher, resource_queue):
        """Spider Engine Initializer 

        Initializes spider engine with configurations

        Args:
            config: Configuration object of spider
            dispatcher: The threads dispatcher
            resource_queue: Resource queue on which actions done
        """
        
        self.config = config
        self.dispatcher = dispatcher
        self.resource_queue = resource_queue

    def start(self):
        """Engine starts here"""

        def perform(resource):
            """Spider action

            The action spider performs on each page defines here.
            Page information and context information are packaged in the resource object

            Args:
                resource: the resource object contains all information
                          spider needs on a page
            """

            #Check whether node level is in range
            config_max_depth = int(self.config.get_config("max_depth"))
            if resource.level > config_max_depth:
                log_msg = "Reached max-depth, abort: {}".format(resource.url)
                logging.info(log_msg)
                return -1

            #Check whether the page url is downloadable
            page_url = resource.url
            if page_url.startswith("javascript"):
                return -1

            #Wait as not to be blocked by host
            craw_interval = int(self.config.get_config("crawl_interval"))
            time.sleep(craw_interval)

            #Pattern match
            is_pattern_matched = True
            target_pattern = self.config.get_config("target_url")
            try:
                pattern = re.compile(target_pattern)
            except Exception as err:
                logging.error("The target_url compiles failed. (%s, %s)" \
                        % (target_pattern, err))
                return -1
            if len(page_url.strip(' ')) < 1 or not pattern.match(page_url.strip(' ')):
                logging.info("Cache only: Pattern not match. (%s, %s)" \
                        % (page_url, target_pattern))
                is_pattern_matched = False

            #Try Download page
            timeout_sec = int(self.config.get_config("crawl_timeout"))
            output_dir = self.config.get_config("output_directory")
            if not is_pattern_matched:
                output_dir = None
            is_download_done, page_content = \
                    util.download(url = page_url, \
                                  dir = output_dir, \
                                  timeout = timeout_sec)
            if not is_download_done or len(page_content) == 0:
                logging.info("Nothing retrieved from: %s" % page_url)
                return -1

            #Parse page urls
            content_url_set = set()
            target_tags = ['img', 'a', 'script', 'style']
            candidate_links = []
            for tag in target_tags:
                candidate_links.extend(BeautifulSoup(page_content, "html.parser").findAll(tag))
            for link in candidate_links:
                if link.has_attr('src'):
                    content_url_set.add(util.extract(link['src'], page_url))
                if link.has_attr('href'):
                    content_url_set.add(util.extract(link['href'], page_url))

            #Wrap parsed urls into resource objects and enqueue
            next_level = resource.level + 1
            queue = resource.queue
            for url in content_url_set:
                res = spider_resource_queue.Resource(url, next_level, queue)
                queue.put(res)
            return 0

        url_file_path = self.config.get_config("url_list_file")
        self.resource_queue.add_from_file(url_file_path)
        self.dispatcher.setup_dispatch_handler(perform)
        self.dispatcher.start_dispatch()
