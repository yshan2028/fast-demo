#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 01:43
# Author:  rongli
# Email:   abc@xyz.com
# File:    process_time.py
# Project: fa-demo
# IDE:     PyCharm
import time

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class ProcessTimeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 在响应头中记录响应时间 """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        start_time = time.time()

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)

        await self.app(scope, receive, send_wrapper)
