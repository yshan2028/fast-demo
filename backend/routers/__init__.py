#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 20:30
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import APIRouter

from .access import router as access_router
from .account import router as account_router
from .ping import router as ping_router
from .role import router as role_router
from .user import router as user_router
from ..config import settings

api_routers = APIRouter(prefix=settings.url_prefix)

if settings.enable_test_router:
    api_routers.include_router(ping_router)

api_routers.include_router(account_router)  # 用户中心

api_routers.include_router(user_router)  # 用户管理
api_routers.include_router(role_router)  # 角色管理
api_routers.include_router(access_router)  # 权限管理
