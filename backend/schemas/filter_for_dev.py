#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-28 11:13
# Author:  rongli
# Email:   abc@xyz.com
# File:    filter_for_dev.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
from typing import Optional

from fastapi import Query

from .base import ORMModel


class UserFilterForDev(ORMModel):
    """  用户表模型(User)的过滤类  """
    id: Optional[int] = Query(None, alias='id', description='id')
    id__isnull: Optional[bool] = Query(None, alias='id__isnull', description='id - isnull')
    id__not_isnull: Optional[bool] = Query(None, alias='id__not_isnull', description='id - not_isnull')
    id__not: Optional[int] = Query(None, alias='id__not', description='id - not')
    id__gte: Optional[int] = Query(None, alias='id__gte', description='id - gte')
    id__gt: Optional[int] = Query(None, alias='id__gt', description='id - gt')
    id__lte: Optional[int] = Query(None, alias='id__lte', description='id - lte')
    id__lt: Optional[int] = Query(None, alias='id__lt', description='id - lt')

    create_time: Optional[datetime.datetime] = Query(None, alias='create_time', description='创建时间')
    create_time__isnull: Optional[bool] = Query(None, alias='create_time__isnull', description='创建时间 - isnull')
    create_time__not_isnull: Optional[bool] = Query(None, alias='create_time__not_isnull',
                                                    description='创建时间 - not_isnull')
    create_time__not: Optional[datetime.datetime] = Query(None, alias='create_time__not', description='创建时间 - not')
    create_time__gte: Optional[datetime.datetime] = Query(None, alias='create_time__gte', description='创建时间 - gte')
    create_time__gt: Optional[datetime.datetime] = Query(None, alias='create_time__gt', description='创建时间 - gt')
    create_time__lte: Optional[datetime.datetime] = Query(None, alias='create_time__lte', description='创建时间 - lte')
    create_time__lt: Optional[datetime.datetime] = Query(None, alias='create_time__lt', description='创建时间 - lt')
    create_time__year: Optional[int] = Query(None, alias='create_time__year', description='创建时间 - year')
    create_time__quarter: Optional[int] = Query(None, alias='create_time__quarter', description='创建时间 - quarter')
    create_time__month: Optional[int] = Query(None, alias='create_time__month', description='创建时间 - month')
    create_time__week: Optional[int] = Query(None, alias='create_time__week', description='创建时间 - week')
    create_time__day: Optional[int] = Query(None, alias='create_time__day', description='创建时间 - day')
    create_time__hour: Optional[int] = Query(None, alias='create_time__hour', description='创建时间 - hour')
    create_time__minute: Optional[int] = Query(None, alias='create_time__minute', description='创建时间 - minute')
    create_time__second: Optional[int] = Query(None, alias='create_time__second', description='创建时间 - second')
    create_time__microsecond: Optional[int] = Query(None, alias='create_time__microsecond',
                                                    description='创建时间 - microsecond')

    update_time: Optional[datetime.datetime] = Query(None, alias='update_time', description='更新时间')
    update_time__isnull: Optional[bool] = Query(None, alias='update_time__isnull', description='更新时间 - isnull')
    update_time__not_isnull: Optional[bool] = Query(None, alias='update_time__not_isnull',
                                                    description='更新时间 - not_isnull')
    update_time__not: Optional[datetime.datetime] = Query(None, alias='update_time__not', description='更新时间 - not')
    update_time__gte: Optional[datetime.datetime] = Query(None, alias='update_time__gte', description='更新时间 - gte')
    update_time__gt: Optional[datetime.datetime] = Query(None, alias='update_time__gt', description='更新时间 - gt')
    update_time__lte: Optional[datetime.datetime] = Query(None, alias='update_time__lte', description='更新时间 - lte')
    update_time__lt: Optional[datetime.datetime] = Query(None, alias='update_time__lt', description='更新时间 - lt')
    update_time__year: Optional[int] = Query(None, alias='update_time__year', description='更新时间 - year')
    update_time__quarter: Optional[int] = Query(None, alias='update_time__quarter', description='更新时间 - quarter')
    update_time__month: Optional[int] = Query(None, alias='update_time__month', description='更新时间 - month')
    update_time__week: Optional[int] = Query(None, alias='update_time__week', description='更新时间 - week')
    update_time__day: Optional[int] = Query(None, alias='update_time__day', description='更新时间 - day')
    update_time__hour: Optional[int] = Query(None, alias='update_time__hour', description='更新时间 - hour')
    update_time__minute: Optional[int] = Query(None, alias='update_time__minute', description='更新时间 - minute')
    update_time__second: Optional[int] = Query(None, alias='update_time__second', description='更新时间 - second')
    update_time__microsecond: Optional[int] = Query(None, alias='update_time__microsecond',
                                                    description='更新时间 - microsecond')

    status: Optional[bool] = Query(None, alias='status', description='True:启用 False:禁用')
    status__isnull: Optional[bool] = Query(None, alias='status__isnull', description='True:启用 False:禁用 - isnull')
    status__not_isnull: Optional[bool] = Query(None, alias='status__not_isnull',
                                               description='True:启用 False:禁用 - not_isnull')

    remark: Optional[str] = Query(None, alias='remark', description='备注描述')
    remark__isnull: Optional[bool] = Query(None, alias='remark__isnull', description='备注描述 - isnull')
    remark__not_isnull: Optional[bool] = Query(None, alias='remark__not_isnull', description='备注描述 - not_isnull')
    remark__not: Optional[str] = Query(None, alias='remark__not', description='备注描述 - not')
    remark__contains: Optional[str] = Query(None, alias='remark__contains', description='备注描述 - contains')
    remark__icontains: Optional[str] = Query(None, alias='remark__icontains', description='备注描述 - icontains')
    remark__startswith: Optional[str] = Query(None, alias='remark__startswith', description='备注描述 - startswith')
    remark__istartswith: Optional[str] = Query(None, alias='remark__istartswith', description='备注描述 - istartswith')
    remark__endswith: Optional[str] = Query(None, alias='remark__endswith', description='备注描述 - endswith')
    remark__iendswith: Optional[str] = Query(None, alias='remark__iendswith', description='备注描述 - iendswith')
    remark__iexact: Optional[str] = Query(None, alias='remark__iexact', description='备注描述 - iexact')
    remark__search: Optional[str] = Query(None, alias='remark__search', description='备注描述 - search')

    username: Optional[str] = Query(None, alias='username', description='用户名')
    username__isnull: Optional[bool] = Query(None, alias='username__isnull', description='用户名 - isnull')
    username__not_isnull: Optional[bool] = Query(None, alias='username__not_isnull', description='用户名 - not_isnull')
    username__not: Optional[str] = Query(None, alias='username__not', description='用户名 - not')
    username__contains: Optional[str] = Query(None, alias='username__contains', description='用户名 - contains')
    username__icontains: Optional[str] = Query(None, alias='username__icontains', description='用户名 - icontains')
    username__startswith: Optional[str] = Query(None, alias='username__startswith', description='用户名 - startswith')
    username__istartswith: Optional[str] = Query(None, alias='username__istartswith',
                                                 description='用户名 - istartswith')
    username__endswith: Optional[str] = Query(None, alias='username__endswith', description='用户名 - endswith')
    username__iendswith: Optional[str] = Query(None, alias='username__iendswith', description='用户名 - iendswith')
    username__iexact: Optional[str] = Query(None, alias='username__iexact', description='用户名 - iexact')
    username__search: Optional[str] = Query(None, alias='username__search', description='用户名 - search')

    password: Optional[str] = Query(None, alias='password', description='密码')
    password__isnull: Optional[bool] = Query(None, alias='password__isnull', description='密码 - isnull')
    password__not_isnull: Optional[bool] = Query(None, alias='password__not_isnull', description='密码 - not_isnull')
    password__not: Optional[str] = Query(None, alias='password__not', description='密码 - not')
    password__contains: Optional[str] = Query(None, alias='password__contains', description='密码 - contains')
    password__icontains: Optional[str] = Query(None, alias='password__icontains', description='密码 - icontains')
    password__startswith: Optional[str] = Query(None, alias='password__startswith', description='密码 - startswith')
    password__istartswith: Optional[str] = Query(None, alias='password__istartswith', description='密码 - istartswith')
    password__endswith: Optional[str] = Query(None, alias='password__endswith', description='密码 - endswith')
    password__iendswith: Optional[str] = Query(None, alias='password__iendswith', description='密码 - iendswith')
    password__iexact: Optional[str] = Query(None, alias='password__iexact', description='密码 - iexact')
    password__search: Optional[str] = Query(None, alias='password__search', description='密码 - search')

    nickname: Optional[str] = Query(None, alias='nickname', description='昵称')
    nickname__isnull: Optional[bool] = Query(None, alias='nickname__isnull', description='昵称 - isnull')
    nickname__not_isnull: Optional[bool] = Query(None, alias='nickname__not_isnull', description='昵称 - not_isnull')
    nickname__not: Optional[str] = Query(None, alias='nickname__not', description='昵称 - not')
    nickname__contains: Optional[str] = Query(None, alias='nickname__contains', description='昵称 - contains')
    nickname__icontains: Optional[str] = Query(None, alias='nickname__icontains', description='昵称 - icontains')
    nickname__startswith: Optional[str] = Query(None, alias='nickname__startswith', description='昵称 - startswith')
    nickname__istartswith: Optional[str] = Query(None, alias='nickname__istartswith', description='昵称 - istartswith')
    nickname__endswith: Optional[str] = Query(None, alias='nickname__endswith', description='昵称 - endswith')
    nickname__iendswith: Optional[str] = Query(None, alias='nickname__iendswith', description='昵称 - iendswith')
    nickname__iexact: Optional[str] = Query(None, alias='nickname__iexact', description='昵称 - iexact')
    nickname__search: Optional[str] = Query(None, alias='nickname__search', description='昵称 - search')

    phone: Optional[str] = Query(None, alias='phone', description='手机号')
    phone__isnull: Optional[bool] = Query(None, alias='phone__isnull', description='手机号 - isnull')
    phone__not_isnull: Optional[bool] = Query(None, alias='phone__not_isnull', description='手机号 - not_isnull')
    phone__not: Optional[str] = Query(None, alias='phone__not', description='手机号 - not')
    phone__contains: Optional[str] = Query(None, alias='phone__contains', description='手机号 - contains')
    phone__icontains: Optional[str] = Query(None, alias='phone__icontains', description='手机号 - icontains')
    phone__startswith: Optional[str] = Query(None, alias='phone__startswith', description='手机号 - startswith')
    phone__istartswith: Optional[str] = Query(None, alias='phone__istartswith', description='手机号 - istartswith')
    phone__endswith: Optional[str] = Query(None, alias='phone__endswith', description='手机号 - endswith')
    phone__iendswith: Optional[str] = Query(None, alias='phone__iendswith', description='手机号 - iendswith')
    phone__iexact: Optional[str] = Query(None, alias='phone__iexact', description='手机号 - iexact')
    phone__search: Optional[str] = Query(None, alias='phone__search', description='手机号 - search')

    email: Optional[str] = Query(None, alias='email', description='邮箱')
    email__isnull: Optional[bool] = Query(None, alias='email__isnull', description='邮箱 - isnull')
    email__not_isnull: Optional[bool] = Query(None, alias='email__not_isnull', description='邮箱 - not_isnull')
    email__not: Optional[str] = Query(None, alias='email__not', description='邮箱 - not')
    email__contains: Optional[str] = Query(None, alias='email__contains', description='邮箱 - contains')
    email__icontains: Optional[str] = Query(None, alias='email__icontains', description='邮箱 - icontains')
    email__startswith: Optional[str] = Query(None, alias='email__startswith', description='邮箱 - startswith')
    email__istartswith: Optional[str] = Query(None, alias='email__istartswith', description='邮箱 - istartswith')
    email__endswith: Optional[str] = Query(None, alias='email__endswith', description='邮箱 - endswith')
    email__iendswith: Optional[str] = Query(None, alias='email__iendswith', description='邮箱 - iendswith')
    email__iexact: Optional[str] = Query(None, alias='email__iexact', description='邮箱 - iexact')
    email__search: Optional[str] = Query(None, alias='email__search', description='邮箱 - search')

    full_name: Optional[str] = Query(None, alias='full_name', description='姓名')
    full_name__isnull: Optional[bool] = Query(None, alias='full_name__isnull', description='姓名 - isnull')
    full_name__not_isnull: Optional[bool] = Query(None, alias='full_name__not_isnull', description='姓名 - not_isnull')
    full_name__not: Optional[str] = Query(None, alias='full_name__not', description='姓名 - not')
    full_name__contains: Optional[str] = Query(None, alias='full_name__contains', description='姓名 - contains')
    full_name__icontains: Optional[str] = Query(None, alias='full_name__icontains', description='姓名 - icontains')
    full_name__startswith: Optional[str] = Query(None, alias='full_name__startswith', description='姓名 - startswith')
    full_name__istartswith: Optional[str] = Query(None, alias='full_name__istartswith',
                                                  description='姓名 - istartswith')
    full_name__endswith: Optional[str] = Query(None, alias='full_name__endswith', description='姓名 - endswith')
    full_name__iendswith: Optional[str] = Query(None, alias='full_name__iendswith', description='姓名 - iendswith')
    full_name__iexact: Optional[str] = Query(None, alias='full_name__iexact', description='姓名 - iexact')
    full_name__search: Optional[str] = Query(None, alias='full_name__search', description='姓名 - search')
    head_img__iendswith: Optional[str] = Query(None, alias='head_img__iendswith', description='头像 - iendswith')
    head_img__iexact: Optional[str] = Query(None, alias='head_img__iexact', description='头像 - iexact')
    head_img__search: Optional[str] = Query(None, alias='head_img__search', description='头像 - search')

    gender: Optional[int] = Query(None, alias='gender', description='unknown: 0 male: 1 female: 2')
    gender__isnull: Optional[bool] = Query(None, alias='gender__isnull',
                                           description='unknown: 0 male: 1 female: 2 - isnull')
    gender__not_isnull: Optional[bool] = Query(None, alias='gender__not_isnull',
                                               description='unknown: 0 male: 1 female: 2 - not_isnull')
    gender__not: Optional[int] = Query(None, alias='gender__not', description='unknown: 0 male: 1 female: 2 - not')
    gender__gte: Optional[int] = Query(None, alias='gender__gte', description='unknown: 0 male: 1 female: 2 - gte')
    gender__gt: Optional[int] = Query(None, alias='gender__gt', description='unknown: 0 male: 1 female: 2 - gt')
    gender__lte: Optional[int] = Query(None, alias='gender__lte', description='unknown: 0 male: 1 female: 2 - lte')
    gender__lt: Optional[int] = Query(None, alias='gender__lt', description='unknown: 0 male: 1 female: 2 - lt')
