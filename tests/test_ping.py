#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 02:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    test_ping.py
# Project: fa-demo
# IDE:     PyCharm
from fastapi.testclient import TestClient
from starlette import status

from backend.config import settings
from backend.schemas import SuccessResp
from backend.server import app

client = TestClient(app)


def test_ping():
    response = client.get(settings.url_prefix + '/test/ping')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == SuccessResp(data={"ping": "pong"}).dict(by_alias=True)


def test_time():
    response = client.get(settings.url_prefix + '/test/time')
    assert response.status_code == status.HTTP_200_OK


def test_sleep():
    response = client.get(settings.url_prefix + '/test/sleep')
    assert response.status_code == status.HTTP_200_OK
