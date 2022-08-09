#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 00:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    base.py
# Project: fa-demo
# IDE:     PyCharm

from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from tortoise.queryset import QuerySet


class ResponseModel(GenericModel):
    """ 可以使用别名的响应模型 """

    class Config:
        allow_population_by_field_name = True


Model = TypeVar('Model', bound='BaseModel')


class ORMModel(BaseModel):
    """ 带orm的pydantic模型 """

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @classmethod
    async def from_queryset(cls: Type['Model'], qs: QuerySet ) -> List["Model"]:
        return [cls.from_orm(x) for x in await qs]


DataT = TypeVar("DataT")  # 响应的数据


class FailResp(ResponseModel, Generic[DataT]):
    """ 失败的响应 """
    code: int = Field(..., gt=0, description='状态码')
    msg: str = Field(..., description='信息摘要', alias='message')
    data: Optional[DataT] = Field(None, description='响应的数据', alias='result')


class SuccessResp(ResponseModel, Generic[DataT]):
    """ 成功的响应 """
    code: int = Field(0, description='状态码')
    msg: str = Field('success', description='信息摘要', alias='message')
    data: Optional[DataT] = Field(None, description='响应的数据', alias='result')


class SingleResp(SuccessResp, Generic[DataT]):
    """ 响应单个对象 """
    data: DataT = Field(..., description='响应的数据', alias='result')


class MultiResp(SuccessResp, Generic[DataT]):
    """ 响应多个对象 """
    data: List[DataT] = Field(..., description='响应的数据', alias='result')


class PageData(GenericModel, Generic[DataT]):
    """ 分页响应的数据部分 """
    total: int = Field(..., description='总数量')
    items: List[DataT]


class PageResp(SuccessResp, Generic[DataT]):
    """ 分页响应 vben """
    data: PageData[DataT] = Field(..., description='响应的数据', alias='result')
