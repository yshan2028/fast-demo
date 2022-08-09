#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 19:12
# Author:  rongli
# Email:   abc@xyz.com
# File:    home.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()


@router.get('/', summary='首页', response_class=HTMLResponse)
async def home(request: Request):
    context = {'request': request}
    return request.app.state.jinja.TemplateResponse("index.html", context=context)


@router.get('/favicon.ico', summary='favicon')
async def home():
    return RedirectResponse('/static/img/favicon.ico')



