#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 23:52
# Author:  rongli
# Email:   abc@xyz.com
# File:    access.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import BaseFilter, ORMModel


class MenuUpdate(ORMModel):
    id: int
    title: str
    icon: Optional[str]
    remark: Optional[str]
    order_no: Optional[int]


class SetAccess(BaseModel):
    """ 给角色设置权限 """
    role_id: int
    access: List[int] = Field(default=[], description="权限集合")


class OperationLogFilter(BaseFilter):
    user_id: int = Query(None, description="用户ID")
    object_cls: str = Query(None, description="操作对象")
    method: str = Query(None, description="操作方法")
    ip: str = Query(None, description="访问IP")


class MenuItem(ORMModel):
    id: int
    order_no: int = Field(..., alias='orderNo')
    create_time: datetime = Field(..., alias='createTime')
    status: bool
    icon: Optional[str]
    component: Optional[str]
    scopes: Optional[str] = Field(..., alias='permission')


class OperationLogItem(ORMModel):
    id: int
    user_id: int
    object_cls: str
    method: str
    ip: str
    remark: str
    detail: Dict
    create_time: datetime = Field(..., alias='createTime')
