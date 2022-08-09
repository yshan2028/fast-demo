#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-29 21:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    permission.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from starlette import status

from .auth import get_current_active_user
from ..models import Access, User


async def check_permissions(security_scopes: SecurityScopes, user: User = Depends(get_current_active_user)):
    # print(security_scopes.scopes)
    # 当前域不需要验证
    if not security_scopes.scopes:
        return

    # 超级管理员(root) 拥有所有权限
    if user.is_superuser:
        return

    # 未查询用户是否有对应权限
    is_pass = await Access.filter(role__user__id=user.pk, scopes__in=set(security_scopes.scopes)).exists()
    if not is_pass:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not permissions",
                headers={"scopes": security_scopes.scope_str},
                )
