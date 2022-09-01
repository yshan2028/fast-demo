#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio
import datetime
import os
import random
import time
from multiprocessing import Process
from typing import Dict, List, Optional

from aioredis import Redis
from fastapi import APIRouter, Cookie, Depends, File, Form, Header, Query, Request, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Field, parse_obj_as, validator
from tortoise import Tortoise
from tortoise.functions import Max
from tortoise.query_utils import Prefetch

from ..config import settings
from ..decorators import cache
from ..dependencies import create_access_token, get_captcha_code, get_redis
from ..models import User, UserProfile
from ..schemas import FailResp, MultiResp, ORMModel, SuccessResp, Token
from ..utils import random_str, sync_to_async

router = APIRouter(prefix='/test', tags=['测试'])


@router.get('/ping', summary='ping')
async def ping(req: Request):
    # print(req.session)
    data = {'ping': 'pong'}
    return SuccessResp(data=data)


@router.get('/sleep', summary='sleep')
async def sleep():
    await asyncio.sleep(1)
    data = {'await': 'sleep'}
    return SuccessResp(data=data)


@router.post("/header", summary="获取 Header 参数")
async def get_header_param(
        param: str = Header(..., description="自定义 Header", example="haha", alias="Authorization")):
    """
    ## 当使用 `Authorization` 或 `authorization` 时，docs界面不会自动发送请求头
    ## 请使用 `Apipost` 或者 `postman` 测试这个接口
    ## 关于参数名自动转换的问题，请查看官方文档 [传送门](https://fastapi.tiangolo.com/zh/tutorial/header-params/#_1)
    """
    return SuccessResp(data={"param": param})


@router.get("/cookie", summary="获取 Cookie 参数")
async def get_cookie_param(param: str = Cookie(None, alias="CocaCola", description="自定义 Cookie", example="PepsiCo")):
    """
    ## 请使用 `Apipost` 或者 `postman` 测试这个接口，在 header 中设置 `cookie` 注意是小写的 `c`
    """
    return SuccessResp(data={"param": param})


@router.post("/files", summary="上传文件 by File")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@router.post("/uploadfile", summary="上传文件 by UploadFile")
async def create_upload_file(myfile: UploadFile):
    # 此处仅做为一个示例，以后可以会抽成一个公共的函数
    # 生成一个新的文件名：原文件名_随机值.原后缀名
    if '.' in myfile.filename:
        file_name = ''.join(myfile.filename.split('.')[:-1])
        file_suffix = myfile.filename.split('.')[-1]
        file_full_name = f"{file_name}_{random_str()}.{file_suffix}"
    else:
        file_full_name = f"{myfile.filename}_{random_str()}"

    # 生成一个目录，支持时间命名
    # 可用的时间日期格式化符号，可以查看下方的链接
    # https://www.runoob.com/python/att-time-strftime.html
    folder_name = datetime.datetime.now().strftime("avatar/%Y/%m/%d")
    folder_path = settings.media_dir / folder_name

    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    # 组合成文件全名
    file_full_path = folder_path / file_full_name

    # 获取文件内容，全部读取到内存中，适用于小文件
    contents = await myfile.read()

    # 异步保存防阻塞
    # 加 sync_to_async 装饰器，不会阻塞整个服务
    @sync_to_async
    def save_file(file_path, content):
        with open(file_path, 'wb') as f:
            f.write(content)

    await save_file(file_full_path, contents)

    # 返回一些信息
    file_url = settings.media_url_prefix + "/" + folder_name + "/" + file_full_name
    data = {"filename": myfile.filename,
            "file_full_name": file_full_name,
            "folder_name": folder_name,
            "file_full_path": str(file_full_path),
            "content_type": myfile.content_type,
            "file_url": file_url}
    return SuccessResp[Dict](data=data)


@router.get('/cache', summary='cache')
@cache("cache_test", ex=5)
async def test_cache(req: Request):
    print(req.session)
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/time', summary='查看服务器时间')
async def server_time():
    data = {'time': datetime.datetime.now()}
    return SuccessResp(data=data)


@router.get('/code', summary='查看图片验证码')
async def code(code_in_redis: str = Depends(get_captcha_code)):
    data = {'code': code_in_redis}
    return SuccessResp(data=data)


@router.post('/token', summary='获取 token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None:
        return FailResp(code=10201, msg='用户名与密码不匹配')
    if not user.check_password(form_data.password):
        return FailResp(code=10201, msg='用户名与密码不匹配')
    access_token = create_access_token(data={"sub": user.username})
    token = Token(access_token=access_token, token_type='bearer')
    data = token.dict(by_alias=False)
    return data


@router.get('/config', summary='查看 FastAPI 配置')
async def config():
    data = {'settings': settings}
    return SuccessResp(data=data)


@router.get('/tortoise/config', summary='查看 tortoise 配置')
async def tortoise_config():
    data = {'tortoise_orm_config': settings.tortoise_orm_config}
    return SuccessResp(data=data)


@router.get('/tortoise/models', summary='查看 tortoise models 配置')
async def tortoise_models():
    data = {'tortoise_orm_model_modules': settings.tortoise_orm_model_modules}
    return SuccessResp(data=data)


@router.get('/redis/get', summary='redis get 测试')
async def redis_set(key: str = Query('key'), redis: Redis = Depends(get_redis)):
    data = await redis.get(key)
    return SuccessResp(data=data)


@router.post('/redis/set', summary='redis set 测试')
async def redis_set(key: str = Form('key'),
                    value: str = Form('value'),
                    seconds: int = Form(60, gt=0),
                    redis: Redis = Depends(get_redis)):
    data = await redis.setex(key, seconds, value)
    return SuccessResp(data=data)


@router.delete('/redis/del', summary='redis del 测试')
async def redis_del(key: str = Query('key'),
                    redis: Redis = Depends(get_redis)):
    data = await redis.delete(key)
    return SuccessResp(data=data)


@router.get('/fail_response', summary='失败的响应')
async def fail_response():
    return FailResp(code=500, msg='测试失败的响应')


@router.get('/orm/oto1', summary='orm 测试 - 一对一展平 - alias 改名')
async def orm_test_oto1():
    class UserInfoProfile(ORMModel):
        id: int
        username: str
        profile__point: Optional[int] = Field(..., alias='point')

    user_list = await User.all().values('id', 'username', 'profile__point')
    data = parse_obj_as(List[UserInfoProfile], user_list)
    return MultiResp[UserInfoProfile](data=data)


@router.get('/orm/oto2', summary='orm 测试 - 一对一嵌套 - Prefetch 改名')
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


@router.get('/orm/mtm1', summary='orm 测试 - 多对多嵌套 - @property 实现')
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


# 格式化时间 pydantic实现
class FormatTime(ORMModel):
    now: datetime.datetime

    @validator('now')
    def passwords_match(cls, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")


@router.get('/time/format1', summary="格式化时间   --  pydantic-validator 实现")
async def format_time1():
    now = datetime.datetime.now()
    temp = FormatTime(now=now)
    return SuccessResp[FormatTime](data=temp)


@router.get('/time/format2', summary="格式化时间   --  property 实现 ")
async def format_time1():
    return SuccessResp[str](data="此处用 @property 也能实现这种效果，懒得写了 ")


"""
select id, username, gender,a.rank_num
from (select *, ROW_NUMBER() over (partition by gender order by rand()) as rank_num from user) a
where a.rank_num <= 3
"""


@router.get('/user/sample', summary='分组抽样')
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


@router.get('/tortoise/raw_sql', summary='小乌龟执行SQL语句')
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


def task_process():
    print('start   pid = ', os.getpid(), datetime.datetime.now())
    for i in range(5):
        print(i, 'pid = ', os.getpid())
        time.sleep(1)
    print('end   pid = ', os.getpid())


@router.get('/new/process', summary='尝试启动一个新的进程')
async def create_process():
    p = Process(target=task_process)
    p.start()
    return SuccessResp(data={'pid': p.pid})
