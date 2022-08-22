#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 02:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_token.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from fastapi.testclient import TestClient

from backend.config import settings
from backend.models import User

username, password = ["admin", 'a12345678']  # 超级管理员


@pytest.mark.anyio
async def test_token(client: TestClient):
    data = {"username": username, "password": password}
    response = client.post(settings.url_prefix + "/test/token", data=data)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    assert response.json().get('access_token')


@pytest.mark.anyio
async def test_superuser():
    user = await User.get_or_none(username=username)
    assert user is not None
    assert user.is_superuser
    assert user.check_password(password)
