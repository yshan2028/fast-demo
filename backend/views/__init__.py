#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 19:12
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import APIRouter

from .home import router as home_router
from .oauth import router as oauth_router

# view_routers = APIRouter(tags=['模板视图'], include_in_schema=False)
view_routers = APIRouter(tags=['模板视图'])

view_routers.include_router(home_router)
view_routers.include_router(oauth_router)
