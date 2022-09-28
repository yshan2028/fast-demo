#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 19:02
# Author:  rongli
# Email:   abc@xyz.com
# File:    start_app.py
# Project: fa-demo
# IDE:     PyCharm

from typer import Typer

from .start_app import start_app
from .start_filter import start_filter

app = Typer()

app.command(name='app', help='start a new app')(start_app)
app.command(name='filter', help='start a new filter model')(start_filter)
