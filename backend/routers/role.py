#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 22:36
# Author:  rongli
# Email:   abc@xyz.com
# File:    role.py
# Project: fa-demo
# IDE:     PyCharm
from typing import List, Union

from aioredis import Redis
from fastapi import APIRouter, Depends, Path, Security
from pydantic import parse_obj_as
from tortoise.exceptions import OperationalError
from tortoise.queryset import F
from tortoise.transactions import in_transaction

from ..dependencies import check_permissions, filter_roles, get_redis, PageSizePaginator
from ..models import Access, Role, User
from ..schemas import (CreateRole, FailResp, MultiResp, PageResp, RoleInfo, RoleInfoOptionItem, RoleStatus, SingleResp,
                       SuccessResp,
                       UpdateRole)

router = APIRouter(prefix='/role', tags=['角色管理'])


@router.get("/options", summary="所有角色下拉选项专用", response_model=MultiResp[RoleInfoOptionItem],
            dependencies=[Security(check_permissions, scopes=["role_options"])])
async def all_roles_options():
    all_roles = await Role.filter(status=True).annotate(role_value=F('id')).order_by('order_no')
    data = parse_obj_as(List[RoleInfoOptionItem], all_roles)
    return MultiResp[RoleInfoOptionItem](data=data)


@router.post("", summary="角色添加", dependencies=[Security(check_permissions, scopes=["role_add"])])
async def create_role(post: CreateRole):
    role = await Role.create(**post.dict())
    # 分配权限
    if post.menu_values:
        accesses = await Access.filter(status=True, id__in=post.menu_values).all()
        await role.access.add(*accesses)
    return SuccessResp(data="创建成功!")


@router.put("/status", summary="角色状态", dependencies=[Security(check_permissions, scopes=["role_status"])])
async def set_role_status(post: RoleStatus):
    role = await Role.get_or_none(pk=post.id)
    if role is None:
        return FailResp(code=30501, msg=f"角色不存在")
    role.status = post.status
    await role.save()
    msg = f"角色 [{role.role_name}] 已"
    msg += "启用" if post.status else "停用"
    return SuccessResp(data=msg)


@router.delete("/{rid}", summary="角色删除", dependencies=[Security(check_permissions, scopes=["role_delete"])])
async def delete_role(rid: int = Path(..., gt=0)):
    role = await Role.get_or_none(pk=rid)
    if role is None:
        return FailResp(code=30201, msg="角色不存在!")
    await Role.filter(pk=rid).delete()
    return SuccessResp(data="删除成功!")


@router.put("/{rid}", summary="角色修改", dependencies=[Security(check_permissions, scopes=["role_update"])])
async def update_role(post: UpdateRole, rid: int = Path(..., gt=0), redis: Redis = Depends(get_redis)):
    role = await Role.get_or_none(pk=rid)
    if role is None:
        return FailResp(code=30301, msg='没有找到这个角色')
    # 使用事务，保证数据完整
    try:
        async with in_transaction():
            # 更新资料
            update_data = post.dict(exclude_unset=True, exclude_none=True)
            await role.update_from_dict(update_data)
            await role.save()
            # 清空权限
            await role.access.clear()
            # 修改权限
            if post.menu_values:
                # 清除缓存
                username_list = await User.filter(role__id=rid).values_list('username', flat=True)
                if username_list:
                    cache_key_list = [f"cache:perm_code:{x}" for x in username_list] + \
                                     [f"cache:router_tree:{x}" for x in username_list]
                    await redis.delete(*cache_key_list)
                accesses = await Access.filter(status=True, id__in=post.menu_values).all()
                # 分配权限
                await role.access.add(*accesses)
            # 首页是必选的
            # home_menu = await Access.get(title='首页')
            # await role.access.add(home_menu)
    except OperationalError:
        return FailResp(code=30301, msg="更新失败!")
    return SuccessResp(data="更新成功!")


@router.get("/{rid}", summary="查看角色", response_model=Union[SingleResp[RoleInfo], FailResp],
            dependencies=[Security(check_permissions, scopes=["role_read"])])
async def read_role(rid: int = Path(..., gt=0)):
    role = await Role.get_or_none(pk=rid)
    if role is None:
        return FailResp(code=30401, msg="角色不存在!")
    data = RoleInfo.from_orm(role)
    return SingleResp[RoleInfo](data=data)


@router.get('', summary="角色列表", response_model=PageResp[RoleInfo],
            dependencies=[Security(check_permissions, scopes=["role_list"])])
async def get_all_role(pg: PageSizePaginator() = Depends(), filters: dict = Depends(filter_roles)):
    role_qs = Role.all().annotate(role_value=F('id')).prefetch_related('access').order_by('order_no')
    page_data = await pg.output(role_qs, filters)
    return PageResp[RoleInfo](data=page_data)
