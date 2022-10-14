#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-10-14 13:52
# Author:  rongli
# Email:   abc@xyz.com
# File:    loguru_handler.py
# Project: fa-demo
# IDE:     PyCharm

import logging
from types import FrameType
from typing import cast

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage(), )
