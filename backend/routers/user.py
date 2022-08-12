#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 00:01
# Author:  rongli
# Email:   abc@xyz.com
# File:    account.py
# Project: fa-demo
# IDE:     PyCharm

from typing import Union

from aioredis import Redis
from fastapi import APIRouter, Depends, Request
from simpel_captcha import img_captcha
from starlette.responses import StreamingResponse

from ..config import settings
from ..dependencies import (create_access_token, get_captcha_code, get_current_active_user, get_redis)
from ..enums import OperationMethod as OpMethod, OperationObject as OpObject
from ..models import User
from ..models.base import OperationLog
from ..schemas import (FailResp, LoginResult, ModifyInfo, ModifyPassword,
                       RoleInfoForLoginResp, SingleResp, SuccessResp, UserInfo,
                       UserLogin, UserRegister)
from ..utils import encrypt_password, verify_password

router = APIRouter(prefix='/user', tags=['用户中心'])


@router.post('', response_model=Union[SingleResp[UserInfo], FailResp], summary='用户注册')
async def register(post: UserRegister, code_in_redis: str = Depends(get_captcha_code)):
    if code_in_redis is None:
        return FailResp(code=10302, msg='验证码已过期')
    if post.code.lower() != code_in_redis:
        return FailResp(code=10303, msg='验证码错误')

    if await User.filter(username=post.username).exists():
        return FailResp(code=10101, msg='当前用户名已被占用')
    post.password = encrypt_password(post.password)
    user = await User.create(**post.dict(exclude={'password2'}))
    user_info = UserInfo.from_orm(user)
    return SingleResp[UserInfo](data=user_info)


@router.get("/captcha", summary='图片验证码')
async def image_captcha(req: Request, redis: Redis = Depends(get_redis)):
    image, text = img_captcha(byte_stream=True)
    session_value = req.session.get(settings.session_cookie_name)
    key = settings.captcha_key.format(session_value)
    await redis.setex(key, settings.captcha_seconds, text.lower())
    return StreamingResponse(content=image, media_type='image/jpeg')


@router.post('/login', response_model=Union[SingleResp[LoginResult], FailResp], summary='用户登陆')
async def login(req: Request, post: UserLogin, code_in_redis: str = Depends(get_captcha_code)):
    if code_in_redis is None:
        return FailResp(code=10302, msg='验证码已过期')
    if post.code.lower() != code_in_redis:
        return FailResp(code=10303, msg='验证码错误')
    user = await User.get_or_none(username=post.username)
    if user is None:
        return FailResp(code=10301, msg='账号与密码不匹配')
    if not verify_password(post.password, user.password):
        return FailResp(code=10301, msg='账号与密码不匹配')
    access_token = create_access_token(data={"sub": user.username})

    await OperationLog.add_log(req, user.pk, OpObject.user, OpMethod.login_by_account, f"用户登陆(ID={user.pk})")
    # 此处只是为了配合前端，返回的信息为是否为管理员，没什么实际用处，只是不想改前端代码而已
    role_name = '超级管理员' if user.is_superuser else "普通管理员"
    role_value = '超级管理员' if user.is_superuser else "普通管理员"
    role_info = RoleInfoForLoginResp(role_name=role_name, value=role_value)
    login_result = LoginResult(id=user.pk, token=access_token, role=role_info)

    return SingleResp[LoginResult](data=login_result)


@router.get('', response_model=Union[SingleResp[UserInfo], FailResp], summary='查看个人信息')
async def get_my_info(me=Depends(get_current_active_user)):
    return SingleResp[UserInfo](data=me)


@router.put('/password', response_model=Union[SuccessResp, FailResp], summary='更改密码')
async def change_password(post: ModifyPassword, me: User = Depends(get_current_active_user)):
    if not verify_password(post.old_password, me.password):
        return FailResp(code=10401, msg='旧密码输入错误')
    hash_password = encrypt_password(post.new_password)
    me.password = hash_password
    await me.save(update_fields=['password'])
    return SuccessResp(data='密码更改成功')


@router.put('', response_model=Union[SingleResp[UserInfo], FailResp], summary='修改个人信息')
async def change_info(req: Request, post: ModifyInfo, me: User = Depends(get_current_active_user)):
    await me.update_from_dict(post.dict(exclude_unset=True, exclude_none=True))
    await me.save()
    await OperationLog.add_log(req, me.pk, OpObject.user, OpMethod.update_object, f"用户修改个人信息({me.pk})")
    user_info = UserInfo.from_orm(me)
    return SingleResp[UserInfo](data=user_info)
