#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 01:41
# Author:  rongli
# Email:   abc@xyz.com
# File:    SetSession.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from ..config import settings
from ..utils import random_str


class SetSessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        """ 设置一个随机字符串的session """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":  # 非http协议
            await self.app(scope, receive, send)
            return

        req = Request(scope, receive, send)
        if not req.session.get(settings.session_cookie_name):
            req.session.setdefault(settings.session_cookie_name, random_str())

        await self.app(scope, receive, send)
