#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 00:09
# Author:  rongli
# Email:   abc@xyz.com
# File:    enums.py
# Project: fa-demo
# IDE:     PyCharm
from enum import IntEnum


class UserGender(IntEnum):
    unknown = 0  # 未知
    male = 1  # 男
    female = 2  # 女
