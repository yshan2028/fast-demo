#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-17 20:54
# Author:  rongli
# Email:   abc@xyz.com
# File:    gunicorn.conf.py
# Project: fa-demo
# IDE:     PyCharm
import multiprocessing

from ..config import settings

# https://docs.gunicorn.org/en/stable/install.html

bind = f'{settings.server_host}:{settings.server_port}'  # 绑定fastapi的端口号
wsgi_app = 'backend.server:app'
workers = multiprocessing.cpu_count() * 2 + 1  # 并行工作进程数
# workers = 2  # 并行工作进程数
worker_class = 'uvicron.workers.UvicornWorker'  # 还可以使用gevent模式，还可以使用sync模式，默认sync模式
threads = 1  # 指定每个工作者的线程数
backlog = 2048  # 监听队列
timeout = 120  # 超过多少秒后工作将被杀掉，并重新启动。一般设置为30秒或更多
worker_connections = 1000  # 设置最大并发量
daemon = False  # 默认False，设置守护进程，将进程交给supervisor管理
debug = True
loglevel = 'debug'
proc_name = 'main'  # 默认None，这会影响ps和top。如果要运行多个Gunicorn实例，需要设置一个名称来区分，这就要安装setproctitle模块。如果未安装
# logger_class = 'gunicron.gologging.Logger'
accesslog = settings.log_dir / 'gunicorn_access.log'
errorlog = settings.log_dir / 'gunicorn_error.log'
pidfile = settings.log_dir / 'gunicron.pid'  # 设置进程文件目录
preload_app = True  # 预加载资源
autorestart = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" " "%(a)s"'  # 设置gunicron访问日志格式，错误日志无法设置

# 下面代码在安装了python，并pip install gunicorn的centos服务器中运行，可以用gunicorn启动main,实现接口访问
# gunicorn -c gunicorn.conf.py main:app -k uvicorn.workers.UvicornWorker
