#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the main module

Authors: Wan Li
Date:    2015/09/02
"""

import sys
import getopt
import logging
import log

import spider_config
import spider_resource_queue
import spider_dispatcher
import spider_engine

def version():
    """Print program version."""

    print "version 3.14.159"


def main():
    """Program entrance."""
    config = spider_config.SpiderConfig()

    #Config logging rules
    logging.log.init_log("./log/spider")

    #Parse console options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:")
    except getopt.GetoptError as err:
        error_msg = "Exception: getopt: %s." % err
        print error_msg
        logging.error(error_msg)
        return -1

    #Proceed params
    if len(opts) == 0:
        print "No config file specified. See -c option."
        return -1

    for opt, arg in opts:
        if opt == "-v":
            version()
            return
        elif opt == "-h":
            print "Usage: python mini_spider/run.py -c spider.conf"
            return
        elif opt == "-c":
            if not config.parse(arg):
                print "Config file malformed."
                return -1
            try:
                num_threads = 1
                cnt_str = config.get_config("thread_count")
                num_threads = int(cnt_str)
                queue = spider_resource_queue.ResourceQueue()
                dispatcher = spider_dispatcher.SpiderDispatcher(num_threads, queue)
                engine = spider_engine.SpiderEngine(config, dispatcher, queue)
                engine.start()
            except Exception as e:
                err_msg = "ERROR: caught exception: {}".format(e)
                logging.error(err_msg)
                return -1
        else:
            print "No config file specified. See -c option."
            pass
    return 0

if __name__ == "__main__":
    main()
