#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:    {{ time_now }}
# Author:  {{ author }}
# Email:   {{ email }}
# File:    {{ file_name }}
# Project: {{ project }}
# IDE:     PyCharm
from datetime import datetime
from typing import List
from fastapi import Query
from pydantic import Field, validator

from backend.schemas import BaseFilter,ORMModel


# =============================  input  ===============================
class {{ model_name }}Create(ORMModel):
    """ 创建一个新的 {{ model_name_lower }} """
    {{ model_name_lower }}_name: str = Field(..., alias="{{ model_name_lower }}Name", description='{{ model_name_lower }}名称')

    @validator('{{ model_name_lower }}_name')
    def check_{{ model_name_lower }}_name(cls, value):
        if length := len(value) > 32:
            raise ValueError(f"{{ model_name_lower }}Name 的长度不得超过32位，当前长度为 {length}")
        return value


class {{ model_name }}Update({{ model_name }}Create):
    """ 修改 {{ model_name_lower }} 的信息"""


class {{ model_name }}Filter(BaseFilter):
    """ 过滤 {{ model_name }} """
    {{ model_name_lower }}_name__icontains: str = Query(None, alias='{{ model_name_lower }}Name')

# =============================  output ===============================
class {{ model_name }}Info(ORMModel):
    """ {{ model_name }}信息 """
    id: int = Field(..., alias='{{ model_name_lower }}Id', description='{{ model_name_lower }}Id')
    {{ model_name_lower }}_name: str = Field(..., alias='{{ model_name_lower }}Name', description='{{ model_name_lower }}名称')
    status: bool = Field(..., alias='{{ model_name_lower }}Status', description="{{ model_name_lower }}状态")
    create_time: datetime = Field(..., alias="createAt", description="创建时间")
    update_time: datetime = Field(..., alias="updateAt", description="更新时间")

    @validator('create_time', 'update_time')
    def format_time(cls, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")


class {{ model_name }}Detail({{ model_name }}Info):
    """ {{ model_name }} 的详情 """
