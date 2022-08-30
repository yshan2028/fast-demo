#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 13:49
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_user_api.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from httpx import AsyncClient

from tests.conftest import username


@pytest.mark.anyio
async def test_me(client_with_token: AsyncClient):
    response = await client_with_token.get("/user")
    assert response.status_code == 200
    assert response.json()['result']['username'] == username
