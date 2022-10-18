#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio

from fastapi import APIRouter

from backend.schemas import FailResp, SuccessResp

router = APIRouter(prefix='/ping', tags=['开发调试 - ping'])


@router.get('', summary='ping')
async def ping():
    data = {'ping': 'pong'}
    return SuccessResp(data=data)


@router.get('/sleep', summary='sleep')
async def sleep():
    await asyncio.sleep(1)
    data = {'await': 'sleep'}
    return SuccessResp(data=data)


@router.get('/fail_response', summary='失败的响应')
async def fail_response():
    return FailResp(code=500, msg='测试失败的响应')
