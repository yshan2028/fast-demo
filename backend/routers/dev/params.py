#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:17
# Author:  rongli
# Email:   abc@xyz.com
# File:    ping.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
from typing import Dict

from fastapi import APIRouter, Cookie, File, Form, Header, UploadFile

from backend.config import settings
from backend.schemas import SuccessResp
from backend.utils import random_str, sync_to_async

router = APIRouter(prefix='/test', tags=['开发调试 - 参数'])


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


@router.post("/form_file", summary="form和file一起使用")
def form_file(file: UploadFile, name: str = Form(...), age: int = Form(...)):
    data = {'name': name, "age": age}
    return {"file": file.filename, "form": data}

# @router.post("/{echo_path:path}", summary="request 对象")
# async def get_request(req: Request, echo_path: str):
#     print(req)
#     return {
#         "path": echo_path,
#         "base_url": req.base_url,
#         "client": req.client,
#         "cookies": req.cookies,
#         "body": await req.body(),
#         "headers": req.headers,
#         "method": req.method,
#         "path_params": req.path_params,
#         "query_params": req.query_params,
#         "scope": {k: str(v) for k, v in req.scope.items()},
#         "url": req.url,
#     }
