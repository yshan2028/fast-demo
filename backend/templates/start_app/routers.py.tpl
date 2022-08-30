#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:    {{ time_now }}
# Author:  {{ author }}
# Email:   {{ email }}
# File:    {{ file_name }}
# Project: {{ project }}
# IDE:     PyCharm
from typing import List, Union

from fastapi import APIRouter, Body, Depends, Path, Security
from pydantic import parse_obj_as
from starlette import status

from backend.dependencies import check_permissions, PageSizePaginator
from backend.schemas import FailResp, MultiResp, PageResp, SingleResp, SuccessResp
from .dependencies import filter_{{ model_name_lower }}s
from .models import {{ model_name }}
from .schemas import {{ model_name }}Create, {{ model_name }}Detail, {{ model_name }}Info, {{ model_name }}Update

router = APIRouter(prefix='/{{ model_name_lower }}', tags=['{{ model_name_lower }}接口'])


@router.post("/bulk", summary="批量添加 {{ model_name_lower }}", response_model=MultiResp[{{ model_name }}Info], status_code=status.HTTP_201_CREATED,
dependencies=[Security(check_permissions, scopes=["bulk_create_{{ model_name_lower }}"])])
async def bulk_create_{{ model_name_lower }}(form_data: List[{{ model_name }}Create]):
{{ model_name_lower }}s = [await {{ model_name }}.create(**x.dict()) for x in form_data]
{{ model_name_lower }}s_info = parse_obj_as(List[{{ model_name }}Info], {{ model_name_lower }}s)
return MultiResp[{{ model_name }}Info](data={{ model_name_lower }}s_info)


@router.put('/
{{ '{' }}{{ model_name_lower }}_id}/status', response_model=Union[SuccessResp, FailResp], summary='改变 {{ model_name_lower }} 的状态',
status_code=status.HTTP_200_OK,
dependencies=[Security(check_permissions, scopes=["change_{{ model_name_lower }}_status"])])
async def modify_{{ model_name_lower }}_by_id({{ model_name_lower }}_id: int = Path(..., gt=0, description='{{ model_name_lower }} ID'),
{{ model_name_lower }}_status: bool = Body(..., description="状态")):
{{ model_name_lower }} = await {{ model_name }}.get_or_none(pk={{ model_name_lower }}_id)
if {{ model_name_lower }} is None:
# 此处的 code=50201 是我随手写的，请根据实际需求来修改
return FailResp(code=50201, msg=f'修改失败，ID={{ '{' }}{{ model_name_lower }}_id} 的对象不存在！')
if {{ model_name_lower }}.status == {{ model_name_lower }}_status:
status_str = "启用" if {{ model_name_lower }}_status else "停用"
return FailResp(code=50201, msg=f'修改失败，ID={{ '{' }}{{ model_name_lower }}_id} 的状态已经为{status_str}，无需修改！')
{{ model_name_lower }}.status = {{ model_name_lower }}_status
await {{ model_name_lower }}.save()
{{ model_name_lower }}_detail = {{ model_name }}Detail.from_orm({{ model_name_lower }})
return SingleResp[{{ model_name }}Detail](data={{ model_name_lower }}_detail)


@router.get("", summary="查看 {{ model_name_lower }} 列表", response_model=PageResp[{{ model_name }}Info],
dependencies=[Security(check_permissions, scopes=["list_{{ model_name_lower }}"])])
async def list_{{ model_name_lower }}(pg: PageSizePaginator = Depends(PageSizePaginator(max_size=50)), filters=Depends(filter_{{ model_name_lower }}s)):
user_qs = {{ model_name }}.all()
page_data = await pg.output(user_qs, filters)
return PageResp[{{ model_name }}Info](data=page_data)


@router.get('/
{{ '{' }}{{ model_name_lower }}_id}', response_model=Union[SingleResp[{{ model_name }}Detail], FailResp], summary='查看 {{ model_name_lower }} 详情',
dependencies=[Security(check_permissions, scopes=["get_{{ model_name_lower }}"])])
async def get_{{ model_name_lower }}_by_id({{ model_name_lower }}_id: int = Path(..., gt=0, description='{{ model_name }} ID')):
{{ model_name_lower }} = await {{ model_name }}.get_or_none(pk={{ model_name_lower }}_id)
if {{ model_name_lower }} is None:
return FailResp(code=50101, msg=f'查看失败，ID={{ '{' }}{{ model_name_lower }}_id} 的对象不存在！')
{{ model_name_lower }}_detail = {{ model_name }}Detail.from_orm({{ model_name_lower }})
return SingleResp[{{ model_name }}Detail](data={{ model_name_lower }}_detail)


@router.post("", summary="添加 {{ model_name_lower }}", response_model=SingleResp[{{ model_name }}Detail], status_code=status.HTTP_201_CREATED,
dependencies=[Security(check_permissions, scopes=["create_{{ model_name_lower }}"])])
async def create_{{ model_name_lower }}(form_data: {{ model_name }}Create):
{{ model_name_lower }} = await {{ model_name }}.create(**form_data.dict())
{{ model_name_lower }}_detail = {{ model_name }}Detail.from_orm({{ model_name_lower }})
{{ 'return SingleResp[' }}{{ model_name }}{{ 'Detail](data=' }}{{ model_name_lower }}_detail)


@router.delete('/{{ '{' }}{{ model_name_lower }}_id}', summary='删除 {{ model_name_lower }}',
dependencies=[Security(check_permissions, scopes=["delete_{{ model_name_lower }}"])])
async def delete_{{ model_name_lower }}_by_id({{ model_name_lower }}_id: int = Path(..., gt=0, description='{{ model_name }} ID')):
{{ model_name_lower }} = await {{ model_name }}.get_or_none(pk={{ model_name_lower }}_id)
if {{ model_name_lower }} is None:
return FailResp(code=50201, msg=f'删除失败，ID={{ '{' }}{{ model_name_lower }}_id} 的对象不存在！')
await {{ model_name_lower }}.delete()
return SuccessResp()


@router.put('/
{{ '{' }}{{ model_name_lower }}_id}', response_model=Union[SuccessResp, FailResp], summary='修改 {{ model_name_lower }}',
status_code=status.HTTP_200_OK,
dependencies=[Security(check_permissions, scopes=["update_{{ model_name_lower }}"])])
async def update_{{ model_name_lower }}_by_id(form_data: {{ model_name }}Update, {{ model_name_lower }}_id: int = Path(..., gt=0, description='{{ model_name }} ID')):
{{ model_name_lower }} = await {{ model_name }}.get_or_none(pk={{ model_name_lower }}_id)
if {{ model_name_lower }} is None:
return FailResp(code=50201, msg=f'修改失败，ID={{ '{' }}{{ model_name_lower }}_id} 的对象不存在！')
await {{ model_name_lower }}.update_from_dict(form_data.dict())
await {{ model_name_lower }}.save()
{{ model_name_lower }}_detail = {{ model_name }}Detail.from_orm({{ model_name_lower }})
return SingleResp[{{ model_name }}Detail](data={{ model_name_lower }}_detail)
