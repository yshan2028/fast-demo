#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 13:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    routers.py
# Project: fa-demo
# IDE:     PyCharm
from typing import List, Union

from fastapi import APIRouter, Body, Depends, Path, Security
from pydantic import parse_obj_as
from starlette import status

from backend.dependencies import check_permissions, PageSizePaginator
from backend.schemas import FailResp, MultiResp, PageResp, SingleResp, SuccessResp
from .models import Item
from .schemas import ItemCreate, ItemDetail, ItemFilter, ItemInfo, ItemUpdate

router = APIRouter(prefix='/item', tags=['item接口'])


@router.post("/bulk", summary="批量添加 item", response_model=MultiResp[ItemInfo], status_code=status.HTTP_201_CREATED,
             dependencies=[Security(check_permissions, scopes=["bulk_create_item"])])
async def bulk_create_item(form_data: List[ItemCreate]):
    items = [await Item.create(**x.dict()) for x in form_data]
    items_info = parse_obj_as(List[ItemInfo], items)
    return MultiResp[ItemInfo](data=items_info)


@router.put('/{item_id}/status', response_model=Union[SuccessResp, FailResp], summary='改变 item 的状态',
            status_code=status.HTTP_200_OK,
            dependencies=[Security(check_permissions, scopes=["change_item_status"])])
async def modify_item_by_id(item_id: int = Path(..., gt=0, description='Item ID'),
                            item_status: bool = Body(..., description="状态")):
    item = await Item.get_or_none(pk=item_id)
    if item is None:
        # 此处的 code=50201 是我随手写的，请根据实际需求来修改
        return FailResp(code=50201, msg=f'修改失败，ID={item_id} 的对象不存在！')
    if item.status == item_status:
        status_str = "启用" if item_status else "停用"
        return FailResp(code=50201, msg=f'修改失败，ID={item_id} 的状态已经为{status_str}，无需修改！')
    item.status = item_status
    await item.save()
    item_detail = ItemDetail.from_orm(item)
    return SingleResp[ItemDetail](data=item_detail)


@router.get("", summary="查看 item 列表", response_model=PageResp[ItemInfo],
            dependencies=[Security(check_permissions, scopes=["list_item"])])
async def list_item(pg: PageSizePaginator = Depends(PageSizePaginator(max_size=50)),
                    filters: ItemFilter = Depends(ItemFilter)):
    user_qs = Item.all()
    page_data = await pg.output(user_qs, filters.dict(exclude_none=True))
    return PageResp[ItemInfo](data=page_data)


@router.get('/{item_id}', response_model=Union[SingleResp[ItemDetail], FailResp], summary='查看 item 详情',
            dependencies=[Security(check_permissions, scopes=["get_item"])])
async def get_item_by_id(item_id: int = Path(..., gt=0, description='Item ID')):
    item = await Item.get_or_none(pk=item_id)
    if item is None:
        return FailResp(code=50101, msg=f'查看失败，ID={item_id} 的对象不存在！')
    item_detail = ItemDetail.from_orm(item)
    return SingleResp[ItemDetail](data=item_detail)


@router.post("", summary="添加 item", response_model=SingleResp[ItemDetail], status_code=status.HTTP_201_CREATED,
             dependencies=[Security(check_permissions, scopes=["create_item"])])
async def create_item(form_data: ItemCreate):
    item = await Item.create(**form_data.dict())
    # 记录日志
    # await OperationLog.add_log(req, req.state.user.id, OpObject.item, OpMethod.create_object,
    #                            f"添加 item(itemIDs={item.pk}) 成功")
    item_detail = ItemDetail.from_orm(item)
    return SingleResp[ItemDetail](data=item_detail)


@router.delete('/{item_id}', summary='删除 item',
               dependencies=[Security(check_permissions, scopes=["delete_item"])])
async def delete_item_by_id(item_id: int = Path(..., gt=0, description='Item ID')):
    item = await Item.get_or_none(pk=item_id)
    if item is None:
        return FailResp(code=50201, msg=f'删除失败，ID={item_id} 的对象不存在！')
    await item.delete()
    return SuccessResp()


@router.put('/{item_id}', response_model=Union[SuccessResp, FailResp], summary='修改 item',
            status_code=status.HTTP_200_OK,
            dependencies=[Security(check_permissions, scopes=["update_item"])])
async def update_item_by_id(form_data: ItemUpdate, item_id: int = Path(..., gt=0, description='Item ID')):
    item = await Item.get_or_none(pk=item_id)
    if item is None:
        return FailResp(code=50201, msg=f'修改失败，ID={item_id} 的对象不存在！')
    await item.update_from_dict(form_data.dict())
    await item.save()
    item_detail = ItemDetail.from_orm(item)
    return SingleResp[ItemDetail](data=item_detail)
