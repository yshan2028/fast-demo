#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import Body

from backend.core.routing import LoggingAPIRouter

# 这一段是为了测试 带记录请求体和响应体的 LoggingAPIRouter

# LoggingAPIRouter 用法
# LoggingAPIRouter 可以接受的参数和 APIRouter一样
# 你甚至可以 from ..core.routing import LoggingAPIRouter as APIRouter
# 直接替换原来的 APIRouter 这样几乎不用改动代码就实现了记录功能

# 如果需要修改记录的内容
# 可以自行修改 backend/core/routing.py 的 LoggingRoute
# 注意 LoggingRoute 末尾没有 r
# LoggingRoute, LoggingRouter 这两个不一样的
# 官方文档的地址：https://fastapi.tiangolo.com/advanced/custom-request-and-route/


router = LoggingAPIRouter(prefix='/logging', tags=['开发调试 - logging body'])


@router.post('/', summary="记录请求体和响应体")
def logging_body(b: str = Body(...)):
    return dict(b=b)
