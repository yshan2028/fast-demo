#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 15:51
# Author:  rongli
# Email:   abc@xyz.com
# File:    tests.py
# Project: fa-demo
# IDE:     PyCharm
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_bulk_create(client_with_token: AsyncClient):
    data = [{"itemName": f"item-{i}"} for i in range(1, 21)]
    resp = await client_with_token.post('/item/bulk', json=data)
    assert resp.status_code == 201
    assert resp.json()['code'] == 0
    item_list = resp.json()['result']
    assert len(item_list) == 20


@pytest.mark.anyio
async def test_list_item(client_with_token: AsyncClient):
    resp = await client_with_token.get('/item')
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    item_list = resp.json()['result']['items']
    assert len(item_list) == 10


@pytest.mark.anyio
async def test_list_item_page(client_with_token: AsyncClient):
    params = {"page": 2, "pageSize": 2}
    resp = await client_with_token.get('/item', params=params)
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    item_list = resp.json()['result']['items']
    assert len(item_list) == 2
    assert item_list[0]['itemName'] == 'item-3'


@pytest.mark.anyio
async def test_create_item(client_with_token: AsyncClient):
    data = {"itemName": "test"}
    resp = await client_with_token.post('/item', json=data)
    assert resp.status_code == 201
    assert resp.json()['code'] == 0
    item = resp.json()['result']
    assert item['itemName'] == 'test'


@pytest.mark.anyio
async def test_get_item_by_id(client_with_token: AsyncClient):
    item_id = 1
    resp = await client_with_token.get(f'/item/{item_id}')
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    item = resp.json()['result']
    assert item['itemId'] == item_id


@pytest.mark.anyio
async def test_update_item_by_id(client_with_token: AsyncClient):
    item_id = 10
    data = {"itemName": "test"}
    resp = await client_with_token.put(f'/item/{item_id}', json=data)
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    item = resp.json()['result']
    assert item['itemName'] == "test"
    resp = await client_with_token.get(f'/item/{item_id}')
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    item = resp.json()['result']
    assert item['itemName'] == "test"


@pytest.mark.anyio
async def test_delete_item_by_id(client_with_token: AsyncClient):
    item_id = 10
    resp = await client_with_token.delete(f'/item/{item_id}')
    assert resp.status_code == 200
    assert resp.json()['code'] == 0


@pytest.mark.anyio
async def test_delete_not_exist_item_by_id(client_with_token: AsyncClient):
    item_id = 99999
    resp = await client_with_token.delete(f'/item/{item_id}')
    assert resp.status_code == 200
    assert resp.json()['code'] > 0


@pytest.mark.anyio
async def test_list_item_filter(client_with_token: AsyncClient):
    params = {"itemName": "m-1"}
    resp = await client_with_token.get('/item', params=params)
    assert resp.status_code == 200
    assert resp.json()['code'] == 0
    assert resp.json()['result']['total'] > 0
    for item in resp.json()['result']['items']:
        assert 'm-1' in item['itemName']
