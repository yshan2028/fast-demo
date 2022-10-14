#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 01:27
# Author:  rongli
# Email:   abc@xyz.com
# File:    shutdown.py
# Project: fa-demo
# IDE:     PyCharm
import datetime

from loguru import logger


# logger = logging.getLogger('fastapi')


def log_shutdown():
    logger.info(f"fastapi shutdown at {datetime.datetime.now()}")
