#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 02:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_token.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from httpx import AsyncClient

from backend.models import User


@pytest.mark.anyio
async def test_token(client: AsyncClient):
    username, password = ["admin_test", "a12345678"]
    assert await User.filter(username=username).count() == 0

    user = await User.create(username=username, password=password)
    await user.set_password(password)

    data = {"username": username, "password": password}
    response = await client.post("/test/token", data=data)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    assert response.json().get('access_token')


@pytest.mark.anyio
async def test_superuser(client: AsyncClient):
    username, password = ["admin", "a12345678"]
    user = await User.get_or_none(username=username)
    assert user is not None
    assert user.is_superuser
    assert user.password is not password
    assert user.check_password(password)
