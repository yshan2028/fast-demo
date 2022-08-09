#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 16:13
# Author:  rongli
# Email:   abc@xyz.com
# File:    auth.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from ..config import settings
from ..models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.swagger_ui_oauth2_redirect_url)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的token，请重新登陆！",
            headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token已过期，请重新登陆！",
                headers={"WWW-Authenticate": f"Bearer {token}"},
                )
    except JWTError:
        raise credentials_exception

    user = await User.get_or_none(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(req: Request, current_user: User = Depends(get_current_user)):
    # 非超级管理员才会检查账号的状态
    if not current_user.is_superuser:
        if not current_user.status:
            raise HTTPException(status_code=401, detail="该账号已被禁用")
    # 把当前用户绑定到request上，方便后面使用
    req.state.user = current_user
    return current_user
