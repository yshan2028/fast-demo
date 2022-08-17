#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-17 20:54
# Author:  rongli
# Email:   abc@xyz.com
# File:    gunicorn.conf.py
# Project: fa-demo
# IDE:     PyCharm

import multiprocessing

from backend.config import settings

# https://docs.gunicorn.org/en/stable/install.html

# 绑定fastapi的端口号
bind = f'{settings.server_host}:{settings.server_port}'

# app
wsgi_app = 'backend.server:app'

# 并行工作进程数
# workers = 2  # 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 还可以使用gevent模式，还可以使用sync模式，默认sync模式
worker_class = 'uvicorn.workers.UvicornWorker'

# 指定每个工作者的线程数
threads = 1

# 监听队列
backlog = 2048

# 超过多少秒后工作将被杀掉，并重新启动。一般设置为30秒或更多
timeout = 120

# 设置最大并发量
worker_connections = 1000

# 默认False，设置守护进程，将进程交给supervisor管理
daemon = False

# 调试模式
debug = False

# 日志等级
loglevel = 'info'

# 默认None，这会影响ps和top。
# 如果要运行多个Gunicorn实例，需要设置一个名称来区分，
# 这就要安装setproctitle模块。如果未安装
proc_name = 'main'

# 日志类
# logger_class = 'gunicron.gologging.Logger'

# 日志位置
accesslog = str(settings.log_dir / 'gunicorn_access.log')
errorlog = str(settings.log_dir / 'gunicorn_error.log')

# 设置gunicron访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" " "%(a)s"'

# 设置进程文件位置
pidfile = str(settings.log_dir / 'gunicorn.pid')

# 预加载资源
preload_app = True

# 自动重启
autorestart = True

# 启动命令
# gunicorn -c gunicorn.conf.py
