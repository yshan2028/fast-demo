#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:    {{ time_now }}
# Author:  {{ author }}
# Email:   {{ email }}
# File:    {{ file_name }}
# Project: {{ project }}
# IDE:     PyCharm
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_bulk_create(client_with_token: AsyncClient):
data = [{"{{ model_name_lower }}Name": f"{{ model_name_lower }}-{i}"} for i in range(1, 21)]
resp = await client_with_token.post('/{{ model_name_lower }}/bulk', json=data)
assert resp.status_code == 201
assert resp.json()['code'] == 0
{{ model_name_lower }}_list = resp.json()['result']
assert len({{ model_name_lower }}_list) == 20


@pytest.mark.anyio
async def test_list_{{ model_name_lower }}(client_with_token: AsyncClient):
resp = await client_with_token.get('/{{ model_name_lower }}')
assert resp.status_code == 200
assert resp.json()['code'] == 0
{{ model_name_lower }}_list = resp.json()['result']['items']
assert len({{ model_name_lower }}_list) == 10


@pytest.mark.anyio
async def test_list_{{ model_name_lower }}_page(client_with_token: AsyncClient):
params = {"page": 2, "pageSize": 2}
resp = await client_with_token.get('/{{ model_name_lower }}', params=params)
assert resp.status_code == 200
assert resp.json()['code'] == 0
{{ model_name_lower }}_list = resp.json()['result']['items']
assert len({{ model_name_lower }}_list) == 2
assert {{ model_name_lower }}_list[0]['{{ model_name_lower }}Name'] == '{{ model_name_lower }}-3'


@pytest.mark.anyio
async def test_create_{{ model_name_lower }}(client_with_token: AsyncClient):
data = {"{{ model_name_lower }}Name": "test"}
resp = await client_with_token.post('/{{ model_name_lower }}', json=data)
assert resp.status_code == 201
assert resp.json()['code'] == 0
{{ model_name_lower }} = resp.json()['result']
assert {{ model_name_lower }}['{{ model_name_lower }}Name'] == 'test'


@pytest.mark.anyio
async def test_get_{{ model_name_lower }}_by_id(client_with_token: AsyncClient):
{{ model_name_lower }}_id = 1
resp = await client_with_token.get(f'/{{ model_name_lower }}/{{ '{' }}{{ model_name_lower }}_id}')
assert resp.status_code == 200
assert resp.json()['code'] == 0
{{ model_name_lower }} = resp.json()['result']
assert {{ model_name_lower }}['{{ model_name_lower }}Id'] == {{ model_name_lower }}_id


@pytest.mark.anyio
async def test_update_{{ model_name_lower }}_by_id(client_with_token: AsyncClient):
{{ model_name_lower }}_id = 10
data = {"{{ model_name_lower }}Name": "test"}
resp = await client_with_token.put(f'/{{ model_name_lower }}/{{ '{' }}{{ model_name_lower }}_id}', json=data)
assert resp.status_code == 200
assert resp.json()['code'] == 0
{{ model_name_lower }} = resp.json()['result']
assert {{ model_name_lower }}['{{ model_name_lower }}Name'] == "test"
resp = await client_with_token.get(f'/{{ model_name_lower }}/{{ '{' }}{{ model_name_lower }}_id}')
assert resp.status_code == 200
assert resp.json()['code'] == 0
{{ model_name_lower }} = resp.json()['result']
assert {{ model_name_lower }}['{{ model_name_lower }}Name'] == "test"


@pytest.mark.anyio
async def test_delete_{{ model_name_lower }}_by_id(client_with_token: AsyncClient):
{{ model_name_lower }}_id = 10
resp = await client_with_token.delete(f'/{{ model_name_lower }}/{{ '{' }}{{ model_name_lower }}_id}')
assert resp.status_code == 200
assert resp.json()['code'] == 0


@pytest.mark.anyio
async def test_delete_not_exist_{{ model_name_lower }}_by_id(client_with_token: AsyncClient):
{{ model_name_lower }}_id = 99999
resp = await client_with_token.delete(f'/{{ model_name_lower }}/{{ '{' }}{{ model_name_lower }}_id}')
assert resp.status_code == 200
assert resp.json()['code'] > 0


@pytest.mark.anyio
async def test_list_{{ model_name_lower }}_filter(client_with_token: AsyncClient):
params = {{ '{' }}"{{ model_name_lower }}Status": True}
resp = await client_with_token.get('/{{ model_name_lower }}', params=params)
assert resp.status_code == 200
assert resp.json()['code'] == 0
assert resp.json()['result']['total'] > 0
for {{ model_name_lower }} in resp.json()['result']['items']:
assert {{ model_name_lower }}['{{ model_name_lower }}Status']
