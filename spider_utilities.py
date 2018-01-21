#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2014 Wan Li. All Rights Reserved
#
################################################################################
"""
This is the utility module, consists several useful auxiliary functions

Authors: Wan Li
Date:    2015/09/02
"""

import urllib2
import socket
import os
import urlparse
import logging

import chardet

def extract(url, base_url):
    """Retrieve standard url.

    Split and complete transformed urls on page content.

    Args:
        url: the transformed url
        base_url: the page URI
    """

    if url.startswith('http') or url.startswith('//'):
        url = urlparse.urlparse(url, scheme='http').geturl()
    else:
        url = urlparse.urljoin(base_url, url)
    return url


def download(url, file_path=None, dir=None, timeout=5):
    """Perform chunked download.

    Perform chunked download in some cases.

    Args:
        url: target url.
        file_path: (optional) the target file to be saved.
        dir: (optional) the target dir to be downloaded.
                if both file_path and dir are None, nothing is saved to local disk
    Return:
        (status, content): (success or not, file string content)
    """

    is_cache_only = False
    if file_path is None and dir is None:
        is_cache_only = True

    try:
        handle = urllib2.urlopen(url = url, timeout = timeout)
        if not is_cache_only and file_path is None:
            if not os.path.exists(dir):
                os.mkdir(dir)
            file_path = os.path.join(dir, url.replace('/', '_')
                                .replace(':', '_')
                                .replace('?', '_').replace('\\', '_'))
        size = handle.info().get("Content-Length")
        if size is None:
            size = -1
        size = int(size)
        actualSize = 0
        blocksize = 64 * 1024

        if file_path is not None:
            fo = open(file_path, "wb")
        content = ""
        while True:
            #May be chunked download here.
            block = handle.read(blocksize)
            actualSize += len(block)
            content += block
            if actualSize > size:
                size = actualSize
            if size == 0:
                size = 1
            if len(block) == 0:
                break
            if file_path is not None:
                file_name = file_path.split("/")[-1]
                status = r"%15s %10d [%3.2f%%]" % \
                        (file_name, actualSize, (actualSize) * 100. / size)
                logging.info(status)
            if file_path is not None:
                fo.write(block)
        if file_path is not None:
            fo.close()

        #Decode content
        encoding = chardet.detect(content)['encoding']
        if encoding == 'GBK':
            pass
        elif encoding == 'GB2312':
            encoding = 'GBK'
        else:
            encoding = 'utf-8'
        try:
            content = content.decode(encoding, 'ignore')
        except Exception as err:
            logging.error("ERROR: could not decode downloaded content. (%s)" % (err))
            return None
        return True, content
    except (urllib2.URLError, socket.timeout) as e:
        logging.error("ERROR: {}".format(e))
        try:
            if file_path is not None:
                fo.close()
        except Exception as err:
            logging.error("ERROR: {}".format(err))
        return False, None
