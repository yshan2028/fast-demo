#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 18:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    only_debug.py
# Project: fa-demo
# IDE:     PyCharm

from ..config import settings


def only_debug(func):
    if settings.debug:
        return func

    def fake_func():
        """
        # 当前接口不可用
        **本接口只有在debug模式下可用**
        """
        return

    return fake_func
