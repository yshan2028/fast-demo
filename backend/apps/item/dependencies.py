#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 13:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    dependencies.py
# Project: fa-demo
# IDE:     PyCharm
from datetime import datetime
from typing import List

from fastapi import Query


def filter_items(item_name: str = Query(None, alias='itemName'), status: bool = Query(None),
                 create_time: List[datetime] = Query(None, alias="createAt")) -> dict:
    query = {}
    if item_name:
        query.setdefault('item_name__icontains', item_name)
    if status is not None:
        query.setdefault('status', status)
    if create_time:
        query.setdefault('create_time__range', create_time)
    return query
