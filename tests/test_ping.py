#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 02:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_ping.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from httpx import AsyncClient
from starlette import status

from backend.schemas import SuccessResp


@pytest.mark.anyio
async def test_ping(client: AsyncClient):
    response = await client.get('/test/ping')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == SuccessResp(data={"ping": "pong"}).dict(by_alias=True)


@pytest.mark.anyio
async def test_time(client: AsyncClient):
    response = await client.get('/test/time')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_sleep(client: AsyncClient):
    response = await client.get('/test/sleep')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_not_found(client: AsyncClient):
    response = await client.get('/x/y/z')
    assert response.status_code == status.HTTP_404_NOT_FOUND
