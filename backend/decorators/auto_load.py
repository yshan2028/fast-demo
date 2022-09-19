#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-19 21:55
# Author:  rongli
# Email:   abc@xyz.com
# File:    auto_load.py
# Project: fa-demo
# IDE:     PyCharm
import functools

from fastapi import APIRouter


def auto_load_router(route: APIRouter, prefix: str, table_name_list: list[str]):
    def decorator(func):
        for table_name in table_name_list:
            @functools.wraps(func)
            def wrapper():
                return func

            route.get(f"/{prefix}/{table_name}", summary=f"自动加载的路由 - {table_name}")(wrapper())

    return decorator
