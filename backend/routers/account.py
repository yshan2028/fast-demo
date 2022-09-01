#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 22:09
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: fa-demo
# IDE:     PyCharm
from typing import Union

from aioredis import Redis
from fastapi import APIRouter, Depends, Path, Request, Security
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from ..dependencies import check_permissions, get_redis, PageSizePaginator
from ..enums import OperationMethod as OpMethod, OperationObject as OpObject
from ..models import OperationLog, Role, User
from ..schemas import (AccountCreate, AccountFilter, AccountInfo, AccountUpdate, FailResp, PageResp, SingleResp,
                       SuccessResp)

router = APIRouter(prefix='/account', tags=['账号管理'])


@router.get('', summary='账号列表', response_model=PageResp[AccountInfo],
            dependencies=[Security(check_permissions, scopes=["account_list"])])
async def get_all_account(pg: PageSizePaginator = Depends(PageSizePaginator()), filters=Depends(AccountFilter)):
    user_qs = User.all().prefetch_related('role')
    page_data = await pg.output(user_qs, filters.dict(exclude_none=True))
    return PageResp[AccountInfo](data=page_data)


@router.get('/{uid}', response_model=Union[SingleResp[AccountInfo], FailResp], summary='查看账号',
            dependencies=[Security(check_permissions, scopes=["account_read"])])
async def get_account_by_id(uid: int = Path(..., gt=0, description='账号ID')):
    user = await User.get_or_none(pk=uid)
    if user is None:
        return FailResp(code=20101, msg=f'查看失败，ID={uid} 的账号不存在！')
    await user.fetch_related('role')
    user_info = AccountInfo.from_orm(user)
    return SingleResp[AccountInfo](data=user_info)


@router.post("", summary="添加用户", dependencies=[Security(check_permissions, scopes=["account_add"])])
async def account_add(req: Request, post: AccountCreate):
    # 过滤用户
    get_user = await User.get_or_none(username=post.username)
    if get_user is not None:
        return FailResp(code=20201, msg=f"账号 {post.username} 已经存在!")

    # 创建用户
    create_user = await User.create(**post.dict())
    await create_user.set_password(post.password)
    await OperationLog.add_log(req, req.state.user.id, OpObject.account, OpMethod.create_object,
                               f"创建账号(ID={create_user.pk})")
    if post.roles:
        # 有分配角色
        roles = await Role.filter(id__in=post.roles, status=True)
        await create_user.role.add(*roles)
        await OperationLog.add_log(req, req.state.user.id, OpObject.account, OpMethod.allocate_resources,
                                   f"分配角色(roleIDs={post.roles})")
    return SuccessResp(data=f"账号 {create_user.username} 创建成功")


@router.delete("/{uid}", summary="删除账号", dependencies=[Security(check_permissions, scopes=["account_delete"])])
async def account_del(req: Request, uid: int = Path(..., gt=0)):
    if req.state.user.pk == uid:
        return FailResp(code=20301, msg="你不能把自己踢出局吧?")
    delete_action = await User.filter(pk=uid).delete()
    if not delete_action:
        return FailResp(code=20302, msg=f"账号{uid}删除失败!")
    await OperationLog.add_log(req, req.state.user.id, OpObject.account, OpMethod.delete_object,
                               f"删除账号(ID={uid})")
    return SuccessResp(data="删除成功")


@router.put("/{uid}", summary="修改账号", dependencies=[Security(check_permissions, scopes=["account_update"])])
async def account_update(req: Request, post: AccountUpdate, uid: int = Path(..., gt=0),
                         redis: Redis = Depends(get_redis)):
    user = await User.get_or_none(pk=uid)
    # 不存在的用户
    if user is None:
        return FailResp(code=20501, msg="用户不存在")
    # 检查用户名是否可用
    if user.username != post.username:
        check_username = await User.get_or_none(username=post.username)
        if check_username:
            return FailResp(code=20502, msg=f"用户名{user.username}已存在")
    # 谁也不能禁用超级管理员的账号
    if user.is_superuser and post.status is False:
        return FailResp(code=20503, msg=f"不能禁用超级管理员")
    # 检查邮箱是否可用
    if post.email and await User.filter(phone=post.email).exists():
        return FailResp(code=20504, msg=f"邮箱 {post.email} 已存在")
    # 使用事务，保证数据完整
    try:
        async with in_transaction():
            # 更新资料
            update_data = post.dict(exclude_unset=True, exclude_none=True)
            await user.update_from_dict(update_data)
            await user.save()
            # 清空角色
            await user.role.clear()
            # 修改权限
            if post.roles:
                # 把缓存清掉
                await redis.delete(f"cache:perm_code:{user.username}", f"cache:router_tree:{user.username}")
                roles = await Role.filter(status=True, id__in=post.roles).all()
                # 分配角色
                await user.role.add(*roles)
    except OperationalError:
        return FailResp(code=20503, msg="更新账号信息失败")
    # 记录你操作日志
    await OperationLog.add_log(req, req.state.user.id, OpObject.account, OpMethod.update_object,
                               f"修改账号(ID={uid})")
    # 开始返回信息
    await user.fetch_related('role')
    data = AccountInfo.from_orm(user)
    return SingleResp[AccountInfo](data=data)
