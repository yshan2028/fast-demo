#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
import os
import time
from multiprocessing import Process

from fastapi import APIRouter, Request
from pydantic import validator

from backend.decorators import auto_load_router
from backend.schemas import ORMModel, SuccessResp

router = APIRouter(prefix='/other', tags=['开发调试 - other'])


# 格式化时间 pydantic实现
class FormatTime(ORMModel):
    now: datetime.datetime

    @validator('now')
    def passwords_match(cls, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")


@router.get('/time/format1', summary="格式化时间   --  pydantic-validator 实现")
async def format_time1():
    now = datetime.datetime.now()
    temp = FormatTime(now=now)
    return SuccessResp[FormatTime](data=temp)


@router.get('/time/format2', summary="格式化时间   --  property 实现 ")
async def format_time1():
    return SuccessResp[str](data="此处用 @property 也能实现这种效果，懒得写了 ")


def task_process():
    print('start   pid = ', os.getpid(), datetime.datetime.now())
    for i in range(5):
        print(i, 'pid = ', os.getpid())
        time.sleep(1)
    print('end   pid = ', os.getpid())


@router.get('/new/process', summary='尝试启动一个新的进程')
async def create_process():
    p = Process(target=task_process)
    p.start()
    return SuccessResp(data={'pid': p.pid})


@auto_load_router(router, prefix="auto/load", table_name_list=['aaa', 'bbb', 'ccc'])
def home(req: Request):
    return {"url_path": req.url.path}
