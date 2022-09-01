#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 22:35
# Author:  rongli
# Email:   abc@xyz.com
# File:    role.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import BaseFilter, ORMModel


# -------------------------------  请求部分  ---------------------------------------------


class CreateRole(BaseModel):
    """ 创建角色 """
    role_name: str = Field(..., alias='roleName')
    status: Optional[bool]
    order_no: Optional[int] = Field(None, alias='orderNo')
    remark: Optional[str]
    menu_values: Optional[List[int]] = Field([], alias='menu')


class UpdateRole(CreateRole):
    """ 更新角色 """


class RoleStatus(BaseModel):
    id: int = Field(..., gt=0)
    status: bool


class RoleFilter(BaseFilter):
    """ 过滤角色 """
    role_name__icontains: str = Query(None, alias='roleName')
    remark__icontains: str = Query(None, alias='remark')


# -------------------------------  响应部分  ---------------------------------------------
class RoleInfoForLoginResp(ORMModel):
    """ 角色信息 用于响应登陆接口 实际返回的是不是超管，只是不想改前端代码而已，实际没什么用 """
    role_name: str = Field(..., alias='roleName', description="用户组")
    value: str = Field(..., description='用户组值')


class RoleInfoOptionItem(ORMModel):
    role_value: int = Field(..., alias='roleValue')
    role_name: str = Field(..., alias='roleName')


class RoleInfo(ORMModel):
    """ 角色信息 """
    id: int
    role_value: int = Field(..., alias='roleValue')
    role_name: str = Field(..., alias='roleName')
    status: bool
    order_no: Optional[int] = Field(..., alias='orderNo')
    create_time: datetime = Field(..., alias='createTime')
    menu_values: Optional[List[int]] = Field([], alias='menu')
    remark: Optional[str]
