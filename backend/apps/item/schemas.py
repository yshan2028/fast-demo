#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 15:55
# Author:  rongli
# Email:   abc@xyz.com
# File:    schemas.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime

from fastapi import Query
from pydantic import Field, validator

from backend.schemas import BaseFilter, ORMModel


# =============================  input  ===============================
class ItemCreate(ORMModel):
    """ 创建一个新的 item """
    item_name: str = Field(..., alias="itemName", description='item名称')

    @validator('item_name')
    def check_item_name(cls, value):
        if length := len(value) > 32:
            raise ValueError(f"itemName 的长度不得超过32位，当前长度为 {length}")
        return value


class ItemUpdate(ItemCreate):
    """ 修改 item 的信息"""


class ItemFilter(BaseFilter):
    item_name__icontains: str = Query(None, alias='itemName')


# =============================  output ===============================
class ItemInfo(ORMModel):
    """ Item信息 """
    id: int = Field(..., alias='itemId', description='itemId')
    item_name: str = Field(..., alias='itemName', description='item名称')
    status: bool = Field(..., alias='itemStatus', description="item状态")
    create_time: datetime = Field(..., alias="createAt", description="创建时间")
    update_time: datetime = Field(..., alias="updateAt", description="更新时间")

    @validator('create_time', 'update_time')
    def format_time(cls, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")


class ItemDetail(ItemInfo):
    """ Item 的详情 """
