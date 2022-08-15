#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-29 22:03
# Author:  rongli
# Email:   abc@xyz.com
# File:    paginator.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio
from typing import Dict, List, Optional

from fastapi import Query
from tortoise.queryset import QuerySet

from ..schemas import PageData


# class PageSizePaginator:
#     def __init__(self, max_size: int = 100):
#         self.max_size = max_size
#
#         self.page_num: int = 1
#         self.page_size: int = 10
#
#     def __call__(self, page_num: int = Query(1, description='当前页码', alias='page'),
#                  page_size: int = Query(10, description='每页数量', alias='pageSize')):
#         self.page_num = max(page_num, 1)  # 如果传入的值小于1，按 1 算
#         self.page_size = min(page_size, self.max_size)  # 如果超过 max_size ， 就算做是 maxsize
#         return self
#
#     async def to_pagination_output(self, queryset: QuerySet, filter_params: Dict, order_by: List[str]):
#         total, items = await asyncio.gather(
#                 queryset.filter(**filter_params).count(),
#                 queryset.limit(self.limit).offset(self.offset).order_by(*order_by).filter(**filter_params),
#                 )
#         return PageData(items=items, total=total)
#
#     @property
#     def limit(self):
#         return self.page_size
#
#     @property
#     def offset(self):
#         return self.page_size * (self.page_num - 1)


class PageSizePaginator:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size

        self.page_num: int = 1
        self.page_size: int = 10

        self.order: List[str] = ['id']

    def __call__(self, page_num: int = Query(1, description='当前页码', alias='page'),
                 page_size: int = Query(10, description='每页数量', alias='pageSize'),
                 order: List[str] = Query(['id'], description='按指定字段排序，格式：id 或 -create_time')):
        self.order = order
        self.page_num = max(page_num, 1)  # 如果传入的值小于1，按 1 算
        self.page_size = min(page_size, self.max_size)  # 如果超过 max_size ， 就算做是 maxsize
        return self

    async def output(self, queryset: QuerySet, filters: Optional[Dict] = None):
        if filters is None:
            filters = {}
        total, items = await asyncio.gather(
                queryset.filter(**filters).count(),
                queryset.limit(self.limit).offset(self.offset).order_by(*self.order).filter(**filters),
                )
        return PageData(items=items, total=total)

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return self.page_size * (self.page_num - 1)
