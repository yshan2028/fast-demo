#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 22:14
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: fa-demo
# IDE:     PyCharm

from tortoise import fields

from .abc import TortoiseBaseModel
from ..enums import UserGender


class User(TortoiseBaseModel):
    username = fields.CharField(unique=True, max_length=20, description="用户名")
    password = fields.CharField(max_length=255, description="密码")
    nickname = fields.CharField(null=True, max_length=255, description='昵称')
    phone = fields.CharField(unique=True, null=True, max_length=11, description="手机号")
    email = fields.CharField(unique=True, null=True, max_length=255, description='邮箱')
    full_name = fields.CharField(null=True, max_length=255, description='姓名')
    is_superuser = fields.BooleanField(default=False, description='是否为超级管理员')
    head_img = fields.CharField(null=True, max_length=255, description='头像')
    gender = fields.IntEnumField(UserGender, default=UserGender.unknown)
    role: fields.ManyToManyRelation["Role"] = fields.ManyToManyField("base.Role", related_name="user",
                                                                     on_delete=fields.CASCADE)
    profile: fields.OneToOneRelation["UserProfile"]

    class Meta:
        table_description = "用户表"
        table = "user"

    def __str__(self):
        return f"<{self.__class__.__name__} username: {self.username}>"

    @property
    def phone_number(self) -> str | None:
        """ 手机号脱敏 """
        if self.phone is None:
            return None
        return f"{self.phone[:3]}****{self.phone[-4:]}"

    @property
    def role_list(self):
        return list(self.role)

    @property
    def role_values(self):
        return [role.pk for role in self.role if role.status]


class Role(TortoiseBaseModel):
    user: fields.ManyToManyRelation["User"]
    role_name = fields.CharField(max_length=15, description="角色名称")

    access: fields.ManyToManyRelation["Access"] = fields.ManyToManyField("base.Access", related_name="role",
                                                                         on_delete=fields.CASCADE)

    class Meta:
        table_description = "角色表"
        table = "role"

    @property
    def menu_values(self):
        return [access.pk for access in self.access]


class Access(TortoiseBaseModel):
    role: fields.ManyToManyRelation[Role]
    # 前端动态生成菜单需要的参数
    path = fields.CharField(null=True, max_length=255, description="路径")
    name = fields.CharField(unique=True, max_length=255, description="名称")
    component = fields.CharField(null=True, max_length=255, description='组件')
    redirect = fields.CharField(null=True, max_length=255, description='重定向')
    # RouteMeta
    title = fields.CharField(unique=True, max_length=255, description="标题")
    icon = fields.CharField(null=True, max_length=255, description="图标")
    hide_children_in_menu = fields.BooleanField(default=False, description="隐藏所有子菜单")
    hide_menu = fields.BooleanField(default=False, description="当前路由不再菜单显示")

    is_router = fields.BooleanField(default=True, description="是否为前端路由")
    is_button = fields.BooleanField(default=False, description="是否为按钮")
    scopes = fields.CharField(null=True, unique=True, max_length=255, description='权限范围标识')
    parent_id = fields.IntField(default=0, description='父id')

    class Meta:
        table_description = "权限表"
        table = "access"

    def __str__(self):
        return f"<Access {self.title} {self.scopes}>"


class UserProfile(TortoiseBaseModel):
    user: fields.OneToOneRelation[User] = fields.OneToOneField('base.User', related_name='profile')
    point = fields.IntField(default=0, description='积分')

    class Meta:
        table_description = "用户扩展资料"
        table = "profile"
