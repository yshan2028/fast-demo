#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-11 17:31
# Author:  rongli
# Email:   abc@xyz.com
# File:    docs.py
# Project: fa-demo
# IDE:     PyCharm

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

from ..config import settings


async def custom_swagger_ui_html(req: Request):
    return get_swagger_ui_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - Swagger UI",
            swagger_js_url=settings.static_url_prefix + "/swagger/swagger-ui-bundle.js",
            swagger_css_url=settings.static_url_prefix + "/swagger/swagger-ui.css",
            swagger_favicon_url=settings.static_url_prefix + "/favicon.ico",
            oauth2_redirect_url=req.app.swagger_ui_oauth2_redirect_url,
            init_oauth=None,
            swagger_ui_parameters=settings.swagger_ui_parameters,
    )


async def custom_redoc_html(req: Request):
    return get_redoc_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - ReDoc",
            redoc_js_url=settings.static_url_prefix + "/redoc/redoc.standalone.js",
            redoc_favicon_url=settings.static_url_prefix + "/favicon.ico",
            with_google_fonts=True,
    )


def custom_docs(app: FastAPI):
    # 只有在debug的时候才启用文档功能
    if settings.debug:
        app.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
        app.get("/redoc", include_in_schema=False)(custom_redoc_html)
