#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm

import datetime
from typing import List, Optional

from aioredis import Redis
from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Field, parse_obj_as, validator
from tortoise.query_utils import Prefetch

from ..config import settings
from ..decorators import cache
from ..dependencies import create_access_token, get_captcha_code, get_redis
from ..models import User, UserProfile
from ..schemas import FailResp, MultiResp, ORMModel, SuccessResp, Token
from ..utils import verify_password

router = APIRouter(prefix='/test', tags=['测试'])


@router.get('/ping', summary='ping')
async def ping(req: Request):
    print(req.session)
    data = {'ping': 'pong'}
    return SuccessResp(data=data)


@router.get('/cache', summary='cache')
@cache("cache_test", ex=5)
async def test_cache(req: Request):
    print(req.session)
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/time', summary='查看服务器时间')
async def server_time():
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/code', summary='查看图片验证码')
async def code(code_in_redis: str = Depends(get_captcha_code)):
    data = {'code': code_in_redis}
    return SuccessResp(data=data)


@router.post('/token', summary='获取 token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None:
        return FailResp(code=10201, msg='用户名与密码不匹配')
    if not verify_password(form_data.password, user.password):
        return FailResp(code=10201, msg='用户名与密码不匹配')
    access_token = create_access_token(data={"sub": user.username})
    token = Token(access_token=access_token, token_type='bearer')
    data = token.dict(by_alias=False)
    return data


@router.get('/config', summary='查看 FastAPI 配置')
async def config():
    data = {'settings': settings}
    return SuccessResp(data=data)


@router.get('/tortoise/config', summary='查看 tortoise 配置')
async def tortoise_config():
    data = {'tortoise_orm_config': settings.tortoise_orm_config}
    return SuccessResp(data=data)


@router.get('/tortoise/models', summary='查看 tortoise models 配置')
async def tortoise_models():
    data = {'tortoise_orm_model_modules': settings.tortoise_orm_model_modules}
    return SuccessResp(data=data)


@router.get('/redis/get', summary='redis get 测试')
async def redis_set(key: str = Query('key'), redis: Redis = Depends(get_redis)):
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


@router.get('/fail_response', summary='失败的响应')
async def fail_response():
    return FailResp(code=500, msg='测试失败的响应')


@router.get('/orm/oto1', summary='orm 测试 - 一对一展平 - alias 改名')
async def orm_test_oto1():
    class UserInfoProfile(ORMModel):
        id: int
        username: str
        profile__point: Optional[int] = Field(..., alias='point')

    user_list = await User.all().values('id', 'username', 'profile__point')
    data = parse_obj_as(List[UserInfoProfile], user_list)
    return MultiResp[UserInfoProfile](data=data)


@router.get('/orm/oto2', summary='orm 测试 - 一对一嵌套 - Prefetch 改名')
async def orm_test_oto2():
    class Profile(ORMModel):
        id: int
        point: int

    class UserInfoProfile(ORMModel):
        id: int
        username: str
        user_profile: Optional[Profile]

    user_qs = User.all().prefetch_related(Prefetch("profile", UserProfile.all(), 'user_profile'))
    data = await UserInfoProfile.from_queryset(user_qs)
    return MultiResp(data=data)


@router.get('/orm/mtm1', summary='orm 测试 - 多对多嵌套 - @property 实现')
async def orm_test_mtm1():
    class RoleInfo(ORMModel):
        id: int
        role_name: str

    class UserInfoProfile(ORMModel):
        id: int
        username: str
        role_list: List[RoleInfo]

    user_qs = User.all().prefetch_related('role')
    data = await UserInfoProfile.from_queryset(user_qs)
    return MultiResp[UserInfoProfile](data=data)


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


@router.get('/time/format2', summary="格式化时间   --  property 实现")
async def format_time1():
    return SuccessResp[str](data="此处用 @property 也能实现这种效果，懒得写了 ")
