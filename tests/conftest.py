#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 03:06
# Author:  rongli
# Email:   abc@xyz.com
# File:    conftest.py.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio

import pytest
from fastapi.testclient import TestClient
from tortoise import generate_schema_for_client, Tortoise

from backend.config import settings
from backend.models import User
from backend.server import app

DB_URL = "sqlite://:memory:"
tortoise_orm_config = settings.tortoise_orm_config
tortoise_orm_config['connections']['default'] = DB_URL


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    yield client


# 注册为一个模块，这样这个函数只会被调用一次，其他的次数都是直接使用第一次调用的结果，功能上类似于@preporty
@pytest.fixture(scope="session")
# ，将这个函数注册为方法，然后在后面使用的时候直接在参数里面注明就行（请参考后面）
def loop():
    loop = asyncio.get_event_loop()
    return loop


async def init_sql():
    username, password = ["admin", 'a12345678']
    user = await User.create(username=username, password=password, is_active=True, is_superuser=True)
    await user.set_password(password)


# 初始化tortoise-orm的连接，autouse自动调用，启动pytest的时候会自动调用
@pytest.fixture(scope="session", autouse=True)
def initialize_tests(loop, request):
    # https://blog.csdn.net/weixin_36179862/article/details/107056267
    loop.run_until_complete(Tortoise.init(config=tortoise_orm_config, _create_db=True))
    # 创建数据库，创建一个临时数据库
    loop.run_until_complete(generate_schema_for_client(Tortoise.get_connection("default"), safe=True))
    # 此处可以初始化一些数据
    loop.run_until_complete(init_sql())
    # 这里使用回调的方式，在左右测试完毕的时候会删除该数据库
    # 尝试删除所有数据库，在所有的数据操作完毕之后回调该方法删除数据库
    request.addfinalizer(lambda: loop.run_until_complete(Tortoise._drop_databases()))
