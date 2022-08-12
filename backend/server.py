#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 20:33
# Author:  rongli
# Email:   abc@xyz.com
# File:    main.py.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError, OperationalError, ValidationError

from .config import settings
from .exceptions import (http422_error_handler, http_error_handler, mysql_does_not_exist, mysql_integrity_error,
                         mysql_operational_error, mysql_validation_error, unicorn_exception_handler, UnicornException)
from .middlewares import BaseMiddleware, LogRequestResponseMiddleware
from .routers import api_routers
from .views import view_routers
from .websocket import ws_router

app = FastAPI(debug=settings.debug,
              docs_url=None,
              redoc_url=None,
              swagger_ui_oauth2_redirect_url=settings.swagger_ui_oauth2_redirect_url,
              title=settings.project_title,
              description=settings.project_description,
              version=settings.project_version,
              default_response_class=ORJSONResponse)

# 只有在debug的时候才启用文档功能
if settings.debug:
    # custom_openapi
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
                description=settings.project_description,
                version=settings.project_version,
                title=settings.project_title,
                routes=app.routes)
        openapi_schema["info"]["x-logo"] = {"url": settings.static_url_prefix + "/logo-teal.png"}
        app.openapi_schema = openapi_schema
        return app.openapi_schema


    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url=settings.static_url_prefix + "/swagger/swagger-ui-bundle.js",
                swagger_css_url=settings.static_url_prefix + "/swagger/swagger-ui.css")


    async def redoc_html():
        return get_redoc_html(
                openapi_url=app.openapi_url,
                title=app.title + " - ReDoc",
                redoc_js_url=settings.static_url_prefix + "/redoc/redoc.standalone.js")


    app.openapi = custom_openapi
    app.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
    app.get("/redoc", include_in_schema=False)(redoc_html)

# 异常错误处理
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)
app.add_exception_handler(DoesNotExist, mysql_does_not_exist)
app.add_exception_handler(IntegrityError, mysql_integrity_error)
app.add_exception_handler(ValidationError, mysql_validation_error)
app.add_exception_handler(OperationalError, mysql_operational_error)

# 注册中间件，先注册的在内层, 洋葱模型
app.add_middleware(LogRequestResponseMiddleware)
app.add_middleware(BaseMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_credentials=settings.cors_allow_credentials,
                   allow_methods=settings.cors_allow_methods,
                   allow_headers=settings.cors_allow_headers)

app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key,
                   session_cookie=settings.session_cookie,
                   max_age=settings.session_max_age)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

# 注册数据库
register_tortoise(app, config=settings.tortoise_orm_config)

# 挂载接口路由
app.include_router(api_routers)
# 挂载视图路由
app.include_router(view_routers)
# 挂载 websocket 路由
app.include_router(ws_router)

# 静态资源目录
app.mount(settings.static_url_prefix, StaticFiles(directory=settings.static_dir), name="static")
# 用户上传目录
app.mount(settings.media_url_prefix, StaticFiles(directory=settings.media_dir), name="media")
# 挂载 jinja2 模板引擎
app.state.jinja = Jinja2Templates(directory=settings.jinja2_templates_dir)
