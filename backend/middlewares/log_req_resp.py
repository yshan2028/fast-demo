#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 17:48
# Author:  rongli
# Email:   abc@xyz.com
# File:    log_req_resp.py
# Project: fa-demo
# IDE:     PyCharm
from logging import getLogger

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from backend.config import settings

logger = getLogger('fastapi')


class LogReqResMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 记录请求体和响应体 """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http",):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        scope_path = scope['path']
        api_path = scope['path'].replace(settings.url_prefix, '')
        if (not scope_path.startswith(settings.url_prefix)) or (api_path in settings.logger_path_white_list):
            await self.app(scope, receive, send)
            return

        if scope.get('server')[0] == 'test':
            await self.app(scope, receive, send)
            return

        receive_ = await receive()

        logger.debug(f"{self.__class__.__name__} request body: {receive_.get('body').decode()}")

        async def receive():
            return receive_

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.body":
                logger.debug(f"{self.__class__.__name__} response body: {message.get('body').decode()}")
            await send(message)

        await self.app(scope, receive, send_wrapper)
