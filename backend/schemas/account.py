#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 20:27
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, validator

from .base import BaseFilter, ORMModel
from .user import check_password, check_username


# -------------------------------  请求部分  ---------------------------------------------

class AccountCreate(BaseModel):
    """ 增加账号 """
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    nickname: Optional[str]
    remark: Optional[str]
    roles: Optional[List[int]]

    _check_username = validator("username", allow_reuse=True)(check_username)
    _check_password = validator("password", allow_reuse=True)(check_password)

    @validator('remark')
    def passwords_match(cls, value, ):
        return value[:10]  # 截断长度超过10的部分


class SetRole(ORMModel):
    """ 给账号设置角色 """
    account_id: int = Field(..., lt=0, alias='accountId', description='账号ID')
    roles: Optional[List[int]] = Field(default=[], description="角色")


class AccountUpdate(ORMModel):
    """ 更新账号 """
    username: str = Field(..., description='用户名')
    nickname: Optional[str]
    email: Optional[EmailStr]
    status: Optional[bool]
    remark: Optional[str]
    roles: List[int] = Field([], description="角色值")


class AccountFilter(BaseFilter):
    """ 过滤用户 """
    username__icontains: Optional[str] = Query(None, alias="username",
                                               description="用户名模糊匹，例如：username='zhangsan'")
    nickname__icontains: Optional[str] = Query(None, alias="nickname")
    email__icontains: Optional[str] = Query(None, alias="email")


# ------------------------------------------------------------------------------------
class AccountInfo(ORMModel):
    """ 账号信息 """
    id: int = Field(..., description='用户ID')
    username: str = Field(..., description='用户名')
    nickname: Optional[str]
    email: Optional[EmailStr]
    create_time: datetime = Field(..., alias="createTime")
    status: bool = Field(..., alias='status')
    remark: Optional[str] = Field(None, description="介绍")
    role_values: List[int] = Field([], description="角色值", alias='roles')
