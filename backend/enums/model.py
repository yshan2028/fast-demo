#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-10 17:49
# Author:  rongli
# Email:   abc@xyz.com
# File:    model.py
# Project: fa-demo
# IDE:     PyCharm

from enum import IntEnum


class UserGender(IntEnum):
    unknown = 0  # 未知
    male = 1  # 男
    female = 2  # 女
