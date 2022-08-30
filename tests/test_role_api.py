#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 14:12
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_account_api.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_list_role(client_with_token: AsyncClient):
    resp = await client_with_token.get('/role')
    assert resp.status_code == 200
    role_list = resp.json()['result']['items']
    assert len(role_list) == 10
