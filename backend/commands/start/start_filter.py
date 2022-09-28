#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-28 09:20
# Author:  rongli
# Email:   abc@xyz.com
# File:    start_filter.py
# Project: fa-demo
# IDE:     PyCharm
from tortoise import Tortoise

from backend.utils import cli_wrapper

# operation 参考文档
# https://tortoise-orm.readthedocs.io/en/latest/query.html#filtering
# in not_in range 请手动处理
# range = gte起点  lte终点


field_operations = {
    "IntField": ["not", "gte", "gt", "lte", "lt"],
    "IntEnumFieldInstance": ["not", "gte", "gt", "lte", "lt"],
    "DatetimeField": ["not", "gte", "gt", "lte", "lt"],
    "BooleanField": [],
    "JSONField": [],
    "CharField": ["not", "contains", "icontains", "startswith", "istartswith", "endswith", "iendswith", "iexact",
                  "search"],
    }
date_part = ["year", "quarter", "month", "week", "day", "hour", "minute", "second", "microsecond"]
null_part = ["isnull", "not_isnull"]


@cli_wrapper
async def start_filter():
    model_list = []
    for app_name, app in Tortoise.apps.items():
        model_list.extend(app.items())
    for index, (model_name, model_cls) in enumerate(model_list):
        print(f"{index:>2}{model_name:>15}  {model_cls}")
    input_index = int(input("请输入模型对应的索引号："))
    model_name, model_cls = model_list[input_index]
    desc = model_cls.describe()
    print('')
    print(f"class {model_name}Filter(BaseFilter):")
    print(f"    \"\"\"  {desc.get('description', 'XX')}模型({model_name})的过滤类  \"\"\"")
    field_list = [desc['pk_field'], *desc['data_fields']]
    for field_dict in field_list:
        field_type = field_dict['field_type']
        # 枚举类型自动生成的描述会有换行，这里面修正一下
        if field_dict['description']:
            field_dict['description'] = field_dict['description'].replace('\n', ' ')
        else:
            field_dict['description'] = field_dict['name']
        # 字段本身
        if field_type not in ['JSONField']:
            print("    {name}:Optional[{python_type}]=Query(None,alias='{name}',"
                  "description='{description}')".format(**field_dict))
        # 关于 null 的查询操作
        for operation in null_part:
            print("    {name}__{operation}:Optional[bool]=Query(None,alias='{name}__{operation}',"
                  "description='{description} - {operation}')".format(**field_dict, operation=operation))
        # 字段扩展的查询操作
        for operation in field_operations[field_type]:
            print("    {name}__{operation}:Optional[{python_type}]=Query(None,alias='{name}__{operation}',"
                  "description='{description} - {operation}')".format(**field_dict, operation=operation))
        # 日期时间型专有的查询操作，不支持 sqlite
        if field_type in ['DatetimeField']:
            for operation in date_part:
                print("    {name}__{operation}:Optional[int]=Query(None,alias='{name}__{operation}',"
                      "description='{description} - {operation}')".format(**field_dict, operation=operation))
        print('')
    print("成功生成过滤类，你可能还需要手动配置别名(alias)、可选项(Optional)")
