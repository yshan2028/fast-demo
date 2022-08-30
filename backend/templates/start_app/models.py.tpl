#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:    {{ time_now }}
# Author:  {{ author }}
# Email:   {{ email }}
# File:    {{ file_name }}
# Project: {{ project }}
# IDE:     PyCharm
from tortoise import fields

from backend.models import TortoiseBaseModel


class {{ model_name }}(TortoiseBaseModel):
""" 在这里写上模型的搭配信息 """
{{ model_name_lower }}_name = fields.CharField(max_length=32, description="名称")

def __str__(self):
return f"{{ model_name }}({self.{{ model_name_lower }}_name}, {self.pk})"

__repr__ = __str__
