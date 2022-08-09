#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 00:11
# Author:  rongli
# Email:   abc@xyz.com
# File:    enums.py
# Project: fa-demo
# IDE:     PyCharm
from enum import IntEnum


class EmailCodeType(IntEnum):
    bind_email = 0
    reset_password = 1