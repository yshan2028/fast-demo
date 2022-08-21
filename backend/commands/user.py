#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 23:38
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: fa-demo
# IDE:     PyCharm
from typer import Abort, Option, secho, Typer
from typer.colors import GREEN, RED

from ..models import User
from ..utils import cli_wrapper

app = Typer()


@app.command()
@cli_wrapper
async def createroot(
        username: str = Option(..., prompt=True),
        password: str = Option(..., prompt=True, confirmation_prompt=True),
        ):
    """Create a root user."""
    try:
        user = await User.create(username=username, password=password, is_superuser=True, is_active=True)
        await user.set_password(password)
        secho(f"Create root user: {user.username}", fg=GREEN)
    except Exception as e:
        secho(e)
        secho("Something went wrong", fg=RED)
        raise Abort()
