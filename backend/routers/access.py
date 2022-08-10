#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-30 23:50
# Author:  rongli
# Email:   abc@xyz.com
# File:    access.py
# Project: fa-demo
# IDE:     PyCharm

from aioredis import Redis
from fastapi import APIRouter, Depends, Security
from starlette.requests import Request
from tortoise.queryset import F

from ..decorators import cache
from ..dependencies import (check_permissions, filter_logs, get_current_active_user, get_redis,
                            PageSizePaginator)
from ..enums import OperationMethod as OpMethod, OperationObject as OpObject
from ..models import Access, User
from ..models.base import OperationLog
from ..schemas import FailResp, MenuUpdate, MultiResp, OperationLogItem, PageResp, SuccessResp
from ..utils import make_tree

router = APIRouter(prefix='/access', tags=['权限管理'])


@router.get('/router_tree', summary="获取前端路由")
@cache("router_tree", ex=24 * 60 * 60)
async def get_router_tree(req: Request, me: User = Depends(get_current_active_user)):
    if me.is_superuser:
        user_menu_ids = await Access.all().values_list('id', flat=True)
    else:
        user_menu_ids = await Access.filter(role__user__id=me.pk).values_list('id', flat=True)
    all_menu_list = [{'id': obj.pk,
                      'path': obj.path,
                      'name': obj.name,
                      'component': obj.component,
                      'redirect': obj.redirect,
                      'order_no': obj.order_no,
                      'meta': {
                          'title': obj.title,
                          'icon': obj.icon,
                          'hideChildrenInMenu': obj.hide_children_in_menu,
                          'hideMenu': obj.hide_menu
                          },
                      'parent_id': obj.parent_id,
                      } for obj in await Access.filter(is_router=True).all()]
    result_list = []

    # all_menu_list 并不能拿到父一级的菜单，所以这里还要修正一下
    # 这一段写得比较丑陋，以后再改吧
    def get_all_menu(menu_ids):
        if not menu_ids:
            return
        temp = []
        for menu_id in menu_ids:
            for menu_item in all_menu_list:
                if menu_id == menu_item['id']:
                    if menu_item not in result_list:
                        result_list.append(menu_item)
                    if menu_item['parent_id'] != 0:
                        temp.append(menu_item['parent_id'])
        get_all_menu(temp)

    get_all_menu(user_menu_ids)
    result_list.sort(key=lambda x: x['order_no'])
    result_list = make_tree(result_list, key_key='id')
    return SuccessResp(data=result_list)


@router.get('/perm_code', response_model=MultiResp[str], summary='获取权限码')
@cache("perm_code", ex=24 * 60 * 60)
async def get_perm_code(req: Request, me: User = Depends(get_current_active_user)):
    if me.is_superuser:
        data = await Access.all().filter(scopes__not_isnull=True).values_list('scopes', flat=True)
    else:
        data = await Access.all().filter(role__user__id=me.pk, scopes__not_isnull=True).values_list('scopes', flat=True)
    return MultiResp[str](data=data)


@router.get('/menu/tree', summary="获取菜单树", dependencies=[Security(check_permissions, scopes=["menu_tree"])])
async def get_menu_tree(req: Request):
    result = await Access.annotate(key=F('id')).all().order_by('order_no', 'id').values('key', 'title', 'parent_id')
    tree_data = make_tree(result)
    return SuccessResp(data=tree_data)


@router.get('/menu/list', summary="菜单管理", dependencies=[Security(check_permissions, scopes=["menu_list"])])
async def get_menu_list():
    result = await Access.annotate(key=F('id'), menuName=F('title')).all().order_by('order_no', 'id') \
        .values('id', 'key', 'title', 'icon', 'parent_id', 'scopes', 'remark', 'menuName', 'order_no')
    tree_data = make_tree(result)
    return SuccessResp(data=tree_data)


@router.put('/menu', summary="修改菜单", dependencies=[Security(check_permissions, scopes=["menu_update"])])
async def menu_update(req: Request, post: MenuUpdate, redis: Redis = Depends(get_redis)):
    menu = await Access.get_or_none(pk=post.id)
    if menu is None:
        return FailResp(code=30101, msg='菜单项不存在')
    data = post.dict(exclude_none=True, exclude_unset=True)
    await menu.update_from_dict(data)
    await menu.save()
    # 如果修改不是最底层的菜单，就清一下缓存，
    if await Access.filter(parent_id=menu.pk).exists():
        username_list = await User.filter(role__access__id=menu.pk).values_list('username', flat=True)
        if username_list:
            perm_code_key_list = [f"cache:perm_code:{x}" for x in username_list]
            router_tree_key_list = [f"cache:router_tree:{x}" for x in username_list]
            await redis.delete(*perm_code_key_list, *router_tree_key_list)
    # 超管的也清一下
    username_list = await User.filter(is_superuser=True).values_list('username', flat=True)
    if username_list:
        perm_code_key_list = [f"cache:perm_code:{x}" for x in username_list]
        router_tree_key_list = [f"cache:router_tree:{x}" for x in username_list]
        await redis.delete(*perm_code_key_list, *router_tree_key_list)
    await OperationLog.add_log(req, req.state.user.id, OpObject.menu, OpMethod.update_object, f"修改菜单(ID={post.id})")
    return SuccessResp(data='修改菜单成功')


@router.get("/operation/logs", summary="查看日志", response_model=PageResp[OperationLogItem],
            dependencies=[Security(check_permissions, scopes=["logs_list"])])
async def get_operation_logs(pg: PageSizePaginator = Depends(PageSizePaginator()), filters=Depends(filter_logs)):
    logs_qs = OperationLog.all()
    page_data = await pg.output(logs_qs, filters)
    return PageResp[OperationLogItem](data=page_data)
