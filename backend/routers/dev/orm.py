#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import random
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import Field, parse_obj_as
from tortoise import Tortoise
from tortoise.expressions import F
from tortoise.functions import Max
from tortoise.query_utils import Prefetch

from backend.config import settings
from backend.models import User, UserProfile
from backend.schemas import MultiResp, ORMModel, SuccessResp, UserFilterForDev

router = APIRouter(prefix='/orm', tags=['开发调试 - orm'])


@router.get('/config', summary='查看 tortoise 配置')
async def tortoise_config():
    data = {'tortoise_orm_config': settings.tortoise_orm_config}
    return SuccessResp(data=data)


@router.get('/models', summary='查看 tortoise models 配置')
async def tortoise_models():
    data = {'tortoise_orm_model_modules': settings.tortoise_orm_model_modules}
    return SuccessResp(data=data)


@router.get('/oto1', summary='orm 测试 - 一对一展平 - alias 改名')
async def orm_test_oto1():
    class UserInfoProfile(ORMModel):
        id: int
        username: str
        profile__point: Optional[int] = Field(..., alias='point')

    user_list = await User.all().values('id', 'username', 'profile__point')
    data = parse_obj_as(List[UserInfoProfile], user_list)
    return MultiResp[UserInfoProfile](data=data)


@router.get('/oto2', summary='orm 测试 - 一对一嵌套 - Prefetch 改名')
async def orm_test_oto2():
    class Profile(ORMModel):
        id: int
        point: int

    class UserInfoProfile(ORMModel):
        id: int
        username: str
        user_profile: Optional[Profile]

    user_qs = User.all().prefetch_related(Prefetch("profile", UserProfile.all(), 'user_profile'))
    data = await UserInfoProfile.from_queryset(user_qs)
    return MultiResp(data=data)


@router.get('/mtm1', summary='orm 测试 - 多对多嵌套 - @property 实现')
async def orm_test_mtm1():
    class RoleInfo(ORMModel):
        id: int
        role_name: str

    class UserInfoProfile(ORMModel):
        id: int
        username: str
        role_list: List[RoleInfo]

    user_qs = User.all().prefetch_related('role')
    data = await UserInfoProfile.from_queryset(user_qs)
    return MultiResp[UserInfoProfile](data=data)


"""
select id, username, gender,a.rank_num
from (select *, ROW_NUMBER() over (partition by gender order by rand()) as rank_num from user) a
where a.rank_num <= 3
"""


@router.get('/sample', summary='分组抽样')
async def get_user_sample():
    gender_list = await User.all().group_by('gender').values_list('gender', flat=True)
    max_id = (await User.all().annotate(max_id=Max('id')).values_list('max_id', flat=True))[0]
    # max_id = (await  User.all().order_by('-id').first()).pk
    res = {str(g): [] for g in gender_list}
    for gender in gender_list:
        key = str(gender)
        user_sample = await User.filter(gender=gender, id__gte=random.randint(1, max_id)).first().values('id',
                                                                                                         'username',
                                                                                                         'gender')
        res[key].append(user_sample)
    return res


@router.get('/raw_sql', summary='小乌龟执行SQL语句')
async def execute_raw_sql():
    """
# 方法汇总
| 方法                | 作用                  | 参数                                      | 返回值                        |  
| ------------------ | -------------------- | ----------------------------------------- | --------------------------- | 
| execute_insert     | 执行查询或插入语句       | query: str, values: list                 |  int                         |
| execute_many       | 执行多条语句           | query: str, values: List[list]            | None                         | 
| execute_query      | 执行查询语句           | query:str,values:Optional[list]=None      | Tuple\[int, Sequence\[dict]] |
| execute_query_dict | 执行查询语句，并返回字典 | query: str, values: Optional[list] = None | List[dict]                   |
| execute_script     | 执行sql脚本           | query: str                                | None                         |

---
# 返回值说明

+ execute_insert: 最后一行的id
+ execute_query: （受影响的行数，结果集）
+ 结果集格式：\[{'id': 1, 'username': 'admin'}, {'id': 2, 'username': 'test'},......\]
+ execute_query_dict: 就是 execute_query 返回值的结果集部分

---
# 注意事项:

+ 上表中的查询语句和插入语句，并没有绝对的界限，底层都是调用了 `cursor.execute`, 我只按他的字面意思进行了翻译
+  拼接 sql 语句时，如果想手动拼接，不要忘记了引号，例如：`sql = "select * from user where username='admin'"`  admin是用引号包上的
+  如果选择传 `values` 的方式， 点位符 %s 不用加引号，底层的包会自动帮忙加上的，下面的 insert_sql 就是这样写的
    """

    conn = Tortoise.get_connection('default')
    select_sql = "select id, username, phone from user limit 3;"
    insert_sql = f"insert into user( username, password) VALUES (%s,%s);"
    res = {
        'execute_insert': await conn.execute_insert(insert_sql, [f"abcd{random.randint(100000, 999999)}", 'a12345678']),
        'execute_many': await conn.execute_many(insert_sql, [[f"abcd{random.randint(100000, 999999)}", 'a12345678']]),
        'execute_query': await conn.execute_query(select_sql),
        'execute_query_dict': await conn.execute_query_dict(select_sql),
        'execute_script': await conn.execute_script(select_sql),
    }
    return SuccessResp(data=res)


@router.get("/describe", summary="查看模型的描述信息")
def orm_describe():
    desc = User.describe()
    return {"desc": desc}


@router.get("/filter", summary="自动生成的过滤类")
def start_filter(filters: UserFilterForDev = Depends(UserFilterForDev)):
    """某些情况下 None 也可能是一个合法的参数，所以 exclude_defaults 更好"""
    return {
        "exclude_defaults": filters.dict(exclude_defaults=True),
        "exclude_unset": filters.dict(exclude_unset=True),
        "exclude_none": filters.dict(exclude_none=True),
    }


class UserAnnotate(ORMModel):
    id: int
    name: str


@router.get('/annotate', response_model=UserAnnotate)
async def annotate():
    lan = 'user' + 'name'
    user = await User.annotate(**{'name': F(lan)}).first()
    return user
