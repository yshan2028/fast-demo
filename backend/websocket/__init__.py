#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-12 18:32
# Author:  rongli
# Email:   abc@xyz.com
# File:    websocket.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import APIRouter

from .visit_count import router as visit_count_router

ws_router = APIRouter(prefix='/ws')

ws_router.include_router(visit_count_router)
