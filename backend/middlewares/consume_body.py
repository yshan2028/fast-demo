#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 01:39
# Author:  rongli
# Email:   abc@xyz.com
# File:    consume_body.py
# Project: fa-demo
# IDE:     PyCharm

from starlette.types import ASGIApp, Receive, Scope, Send

from backend.config import settings


class ConsumeBodyMiddleware:
    """ 可以多次消费诗体 """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return
        # 放行白名单中的路径，流响应和请求，如果不放行，会阻塞
        scope_path = scope['path']
        api_path = scope['path'].replace(settings.url_prefix, '')
        if (not scope_path.startswith(settings.url_prefix)) or (api_path in settings.logger_path_white_list):
            await self.app(scope, receive, send)
            return

        # 以下三行保证请求体可以反复消费
        receive_ = await receive()

        async def receive():
            return receive_

        await self.app(scope, receive, send)
