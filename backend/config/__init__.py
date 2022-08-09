#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:06
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: fa-demo
# IDE:     PyCharm
from .conf import Settings

settings = Settings()
tortoise_orm_config = settings.tortoise_orm_config
