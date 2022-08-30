#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 22:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: fa-demo
# IDE:     PyCharm
from tortoise import fields, Model


class TortoiseBaseModel(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    status = fields.BooleanField(default=True, description='True:启用 False:禁用')
    remark = fields.CharField(null=True, max_length=255, description="备注描述")


    class Meta:
        abstract = True