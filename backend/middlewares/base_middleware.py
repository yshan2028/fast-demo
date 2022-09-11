#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-29 17:16
# Author:  rongli
# Email:   abc@xyz.com
# File:    base_middleware.py
# Project: fa-demo
# IDE:     PyCharm
import time

from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from ..config import settings
from ..utils import random_str


class ProcessTime:
    """
    Middleware
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get(settings.session_cookie_name):
            req.session.setdefault(settings.session_cookie_name, random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = (time.time() - start_time) * 1000
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", f"{process_time:.3f}ms")
            await send(message)

        await self.app(scope, receive, send_wrapper)
