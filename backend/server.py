#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 20:33
# Author:  rongli
# Email:   abc@xyz.com
# File:    main.py.py
# Project: fa-demo
# IDE:     PyCharm
import logging

from aioredis.exceptions import ConnectionError as RedisConnectionError
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import (DBConnectionError as MysqlConnectionError, DoesNotExist as MysqlDoesNotExist,
                                 IntegrityError as MysqlIntegrityError, OperationalError as MysqlOperationalError,
                                 ValidationError as MysqlValidationError)

from .config import settings
from .events import log_shutdown, log_startup, show_logo
from .exceptions import (http422_error_handler, http_error_handler, mysql_connection_error, mysql_does_not_exist,
                         mysql_integrity_error,
                         mysql_operational_error, mysql_validation_error, redis_connection_error,
                         unicorn_exception_handler, UnicornException)
from .middlewares import ProcessTimeMiddleware, SetSessionMiddleware
from .routers import api_routers, custom_docs
from .views import view_routers
from .websocket import ws_router

# 配置日志器
logger.configure(**settings.loguru_config)
# 获取当前所有日志器的名字
logger_name_list = [name for name in logging.root.manager.loggerDict]
logger.debug(sorted(logger_name_list))
# logger.debug('debug')
# logger.info('info')
# logger.warning('warning')
# logger.error('error')
# logger.critical('critical')

# 创建 FastAPI 对象
app = FastAPI(debug=settings.debug,
              docs_url=None,
              redoc_url=None,
              swagger_ui_oauth2_redirect_url=settings.swagger_ui_oauth2_redirect_url,
              title=settings.project_title,
              description=settings.project_description,
              version=settings.project_version,
              default_response_class=ORJSONResponse)

# 自定义文档界面
custom_docs(app)

# 异常错误处理
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)
app.add_exception_handler(MysqlConnectionError, mysql_connection_error)
app.add_exception_handler(MysqlDoesNotExist, mysql_does_not_exist)
app.add_exception_handler(MysqlIntegrityError, mysql_integrity_error)
app.add_exception_handler(MysqlValidationError, mysql_validation_error)
app.add_exception_handler(MysqlOperationalError, mysql_operational_error)
app.add_exception_handler(RedisConnectionError, redis_connection_error)

# 注册中间件，先注册的在内层, 洋葱模型
app.add_middleware(ProcessTimeMiddleware)
# app.add_middleware(LogReqResMiddleware)
app.add_middleware(SetSessionMiddleware)
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

# 注册启动事件
app.add_event_handler('startup', show_logo)
app.add_event_handler('startup', log_startup)
# 注册停止事件
app.add_event_handler('shutdown', log_shutdown)

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
