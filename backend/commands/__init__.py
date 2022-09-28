#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 23:18
# Author:  rongli
# Email:   abc@xyz.com
# File:    commands.py
# Project: fa-demo
# IDE:     PyCharm
from typer import Typer

from .run import app as run_app
from .start import app as start_app
from .user import app as user_app

all_apps = Typer()

all_apps.add_typer(run_app, name="run", help='run some commands')
all_apps.add_typer(user_app, name="user", help='manage your users')
all_apps.add_typer(start_app, name="start", help='start new application')

app = all_apps
