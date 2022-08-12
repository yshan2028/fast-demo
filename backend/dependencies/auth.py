#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 16:13
# Author:  rongli
# Email:   abc@xyz.com
# File:    auth.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from ..config import settings
from ..models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.swagger_ui_oauth2_redirect_url)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_user_or_none_by_token(token: str) -> Union[User, None]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
    except jwt.ExpiredSignatureError:
        return None
    except JWTError:
        return None
    user = await User.get_or_none(username=username)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token已失效，请重新登陆！",
            headers={"WWW-Authenticate": "Bearer"})
    user = await get_user_or_none_by_token(token)
    if user is None:
        raise credentials_exception
    return user


def check_user_status(current_user: User) -> bool:
    # 非超级管理员才会检查账号的状态
    if current_user.is_superuser or current_user.status:
        return True
    else:
        return False


async def get_current_active_user(req: Request, current_user: User = Depends(get_current_user)):
    if check_user_status(current_user):
        # 把当前用户绑定到request上，方便后面使用
        req.state.user = current_user
        return current_user
    else:
        raise HTTPException(status_code=401, detail="该账号已被禁用")
