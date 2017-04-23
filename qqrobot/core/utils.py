#!/usr/bin/env python
# coding:utf-8

import logging

import requests

from config import STORE_LOG, LOG_NAME


def create_logger(log_name=LOG_NAME, store=STORE_LOG):
    logger = logging.getLogger("QQRobot")
    logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    steam.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    if store is True:
        logfile = logging.FileHandler(log_name, mode='a')
        logfile.setLevel(logging.INFO)
        logfile.setFormatter(formatter)
        logger.addHandler(stream)
    return logger

def bknHash(skey, init_str=5381):
    """算法来自https://github.com/pandolia/qqbot
    """
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str


class HTTPRequest(object):
    """HTTP 请求处理基础类
    """
    session = requests.Session()
    session.headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        ),
        "Referer": "http://w.qq.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Connection": "keep-alive",
    }
    def __init__(self, *args, **kw):
        self.session.headers.update(kw)

    def update_headers(self, **kw):
        self.session.headers.update(kw)

    def get(self, url, timeout=30, **args):
        return self.session.get(url, timeout=timeout, **args)

    def post(self, url, timeout=30, **args):
        return self.session.post(url, timeout=timeout, **args)

    def put(self, *args, **kw):
        raise NotImplementedError

    def delete(self, *args, **kw):
        raise NotImplementedError
