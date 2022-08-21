#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 01:27
# Author:  rongli
# Email:   abc@xyz.com
# File:    startup.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
import logging

from ..config import settings

logger = logging.getLogger('fastapi')


def log_startup():
    logger.info(f"fastapi startup at {datetime.datetime.now()}")


def show_logo():
    logo_path = settings.base_dir / 'logo.txt'
    logger.info(logo_path.read_text(encoding='utf8'))
