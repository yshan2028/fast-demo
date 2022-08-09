#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-29 21:09
# Author:  rongli
# Email:   abc@xyz.com
# File:    admin.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime
from typing import List, Optional

from fastapi import Depends, Query
from pydantic import BaseModel


class UserFilter(BaseModel):
    username__icontains: Optional[str] = Query(None, alias="username",
                                               description="用户名模糊匹，例如：username='zhangsan'")
    nickname__icontains: Optional[str] = Query(None, alias="nickname")
    email__icontains: Optional[str] = Query(None, alias="email")
    status: Optional[bool] = Query(None)


def filter_users(filters: UserFilter = Depends(UserFilter),
                 create_time: List[datetime] = Query(None, alias='createTime')):
    # List[datetime] 不能放到 pydantic 模型里面，会搞到 body里面，想不明白，先这样吧
    query = filters.dict(exclude_none=True, exclude_defaults=True)
    if create_time:
        query.setdefault('create_time__range', create_time)
    return query


def filter_roles(role_name: str = Query(None, alias='roleNme'), status: bool = Query(None),
                 create_time: List[datetime] = Query(None)):
    query = {}
    if role_name:
        query.setdefault('role_name__icontains', role_name)
    if status is not None:
        query.setdefault('role_status', status)
    if create_time:
        query.setdefault('create_time__range', create_time)
    return query
