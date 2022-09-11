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


# if settings.debug:
# custom_openapi
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#             description=settings.project_description,
#             version=settings.project_version,
#             title=settings.project_title,
#             routes=app.routes)
#     openapi_schema["info"]["x-logo"] = {"url": settings.static_url_prefix + "/logo-teal.png"}
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
# app.openapi = custom_openapi

async def custom_swagger_ui_html(req: Request):
    return get_swagger_ui_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - Swagger UI",
            oauth2_redirect_url=req.app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.static_url_prefix + "/swagger/swagger-ui-bundle.js",
            swagger_css_url=settings.static_url_prefix + "/swagger/swagger-ui.css")


async def custom_redoc_html(req: Request):
    return get_redoc_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - ReDoc",
            redoc_js_url=settings.static_url_prefix + "/redoc/redoc.standalone.js")


def custom_docs(app: FastAPI):
    # 只有在debug的时候才启用文档功能
    if settings.debug:
        app.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
        app.get("/redoc", include_in_schema=False)(custom_redoc_html)
