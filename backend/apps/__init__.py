#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 13:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import APIRouter

# 把模型集中起来
from .item.models import Item
# 导入路由
from .item.routers import router as item_router
# from .task.routers import router as task_router
# 导入配置
from ..config import settings

# from .task.models import Task

# 把路由集中起来
apps_routers = APIRouter(prefix=settings.url_prefix)
apps_routers.include_router(item_router)
# apps_routers.include_router(task_router)
