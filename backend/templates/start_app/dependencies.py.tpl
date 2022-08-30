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


def filter_{{ model_name_lower }}s({{ model_name_lower }}_name: str = Query(None, alias='{{ model_name_lower }}Name'),
status: bool = Query(None),
create_time: List[datetime] = Query(None, alias="createAt")) -> dict:
query = {}
if {{ model_name_lower }}_name:
query.setdefault('{{ model_name_lower }}_name__icontains', {{ model_name_lower }}_name)
if status is not None:
query.setdefault('status', status)
if create_time:
query.setdefault('create_time__range', create_time)
return query
