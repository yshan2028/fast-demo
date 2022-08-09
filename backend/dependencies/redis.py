#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 21:29
# Author:  rongli
# Email:   abc@xyz.com
# File:    redis.py
# Project: fa-demo
# IDE:     PyCharm
from functools import lru_cache

import aioredis
from aioredis import Redis
from fastapi import Depends, Request

from ..config import settings


@lru_cache()
def get_redis() -> Redis:
    redis = aioredis.from_url(settings.cache_redis_url, encoding='utf-8', decode_responses=True)
    return redis


def get_session_value(req: Request):
    return req.session.get(settings.session_cookie_name)


async def get_captcha_code(session_value: str = Depends(get_session_value),
                           redis: Redis = Depends(get_redis)):
    if session_value is None:
        return
    key = settings.captcha_key.format(session_value)
    code_in_redis = await redis.get(key)
    return code_in_redis
