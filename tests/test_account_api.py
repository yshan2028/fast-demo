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
async def test_list_account(client_with_token: AsyncClient):
    resp = await client_with_token.get('/account')
    assert resp.status_code == 200
    account_list = resp.json()['result']['items']
    assert len(account_list) == 10


@pytest.mark.anyio
async def test_list_account_page(client_with_token: AsyncClient):
    params = {"page": 2, "pageSize": 10}
    resp = await client_with_token.get('/account', params=params)
    assert resp.status_code == 200
    account_list = resp.json()['result']['items']
    assert len(account_list) == 10
