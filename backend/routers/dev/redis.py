#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import datetime

from aioredis import Redis
from fastapi import APIRouter, Depends, Form, Query, Request

from backend.decorators import cache
from backend.dependencies import get_redis
from backend.schemas import SuccessResp

router = APIRouter(prefix='/redis', tags=['开发调试 - redis'])


@router.get('/cache', summary='cache')
@cache("cache_test", ex=5)
async def test_cache(req: Request):
    print(req.session)
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/redis/get', summary='redis get 测试')
async def redis_get(key: str = Query('key'), redis: Redis = Depends(get_redis)):
    data = await redis.get(key)
    return SuccessResp(data=data)


@router.post('/redis/set', summary='redis set 测试')
async def redis_set(key: str = Form('key'),
                    value: str = Form('value'),
                    seconds: int = Form(60, gt=0),
                    redis: Redis = Depends(get_redis)):
    data = await redis.setex(key, seconds, value)
    return SuccessResp(data=data)


@router.delete('/redis/del', summary='redis del 测试')
async def redis_del(key: str = Query('key'),
                    redis: Redis = Depends(get_redis)):
    data = await redis.delete(key)
    return SuccessResp(data=data)
