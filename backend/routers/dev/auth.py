#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.dependencies import create_access_token, get_captcha_code
from backend.models import User
from backend.schemas import FailResp, SuccessResp, Token

router = APIRouter(prefix='/auth', tags=['开发调试 - 认证'])


@router.get('/code', summary='查看图片验证码')
async def code(code_in_redis: str = Depends(get_captcha_code)):
    data = {'code': code_in_redis}
    return SuccessResp(data=data)


@router.post('/token', summary='获取 token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None:
        return FailResp(code=10201, msg='用户名与密码不匹配')
    if not user.check_password(form_data.password):
        return FailResp(code=10201, msg='用户名与密码不匹配')
    access_token = create_access_token(data={"sub": user.username})
    token = Token(access_token=access_token, token_type='bearer')
    data = token.dict(by_alias=False)
    return data
