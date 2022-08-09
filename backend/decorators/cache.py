#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-08 17:51
# Author:  rongli
# Email:   abc@xyz.com
# File:    cache.py
# Project: fa-demo
# IDE:     PyCharm
import functools
import inspect
from typing import Optional

import orjson as json
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

from ..config import settings
from ..dependencies import get_redis


def cache(cache_name: str, ex: Optional[int] = None):
    """
    确定用户唯一的方法
    如果是已经使用 , me: User = Depends(get_current_active_user)
    或者 dependencies=[Security(check_permissions, scopes=["xyx"])] 时
    使用username 否则 使用 SetSessionMiddleware 放置的session
    使用这个装饰器的函数的第一个参数必须是 req: Request
    :param cache_name: 要缓存的内容的名称
    :param ex: 过期时间，不指定就是永久
    """

    def decorator(afunc):
        @functools.wraps(afunc)
        async def wrapper(req: Request, *args, **kwargs):
            sig = inspect.signature(afunc)
            if 'req' not in sig.parameters:
                raise ValueError("使用 cache 装饰器时，第一个参数必须是 req: Request")
            if hasattr(req.state, 'user'):
                cache_key = f"cache:{cache_name}:{req.state.user.username}"
            else:
                cache_key = f"cache:{cache_name}:{req.session.get(settings.session_cookie_name)}"
            redis = get_redis()
            cache_data = await redis.get(cache_key)
            if cache_data is not None:
                return json.loads(cache_data)
            else:
                response = await afunc(req, *args, **kwargs)
                cache_data = json.dumps(jsonable_encoder(response))
                await redis.set(cache_key, cache_data, ex=ex)
                return response

        return wrapper

    return decorator
