#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 13:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    models.py
# Project: fa-demo
# IDE:     PyCharm
from tortoise import fields

from backend.models import TortoiseBaseModel


class Item(TortoiseBaseModel):
    item_name = fields.CharField(max_length=32, description="名称")

    def __str__(self):
        return f"Item({self.item_name}, {self.pk})"

    __repr__ = __str__
