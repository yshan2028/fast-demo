#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
import sys

import fastapi
from fastapi import APIRouter

from backend.config import settings
from backend.schemas import SuccessResp

router = APIRouter(prefix='/system', tags=['开发调试 - 系统配置'])


@router.get('/time', summary='查看服务器时间')
async def server_time():
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/config', summary='查看 FastAPI 配置')
async def config():
    data = {'settings': settings}
    return SuccessResp(data=data)


@router.get("/python", summary='python 相关信息')
def get_python_info():
    return {
        "version": f"Python {sys.version} on {sys.platform}",
        "sys.path": sys.path,
        "fastapi": {"module": str(fastapi).replace("\\\\", "\\"),
                    "version": fastapi.__version__, },
    }
