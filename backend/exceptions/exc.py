#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-31 01:04
# Author:  rongli
# Email:   abc@xyz.com
# File:    exc.py
# Project: fa-demo
# IDE:     PyCharm
class UnicornException(Exception):

    def __init__(self, code, errmsg, data=None):
        """
        失败返回格式
        :param code:
        :param errmsg:
        """
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data
