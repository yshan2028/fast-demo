#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-30 19:02
# Author:  rongli
# Email:   abc@xyz.com
# File:    start_app.py
# Project: fa-demo
# IDE:     PyCharm
import datetime
import re
from typing import List

from jinja2 import Environment, PackageLoader
from typer import prompt, secho, Typer
from typer.colors import GREEN, RED

from backend.config import settings

app = Typer()


def check_dir(app_name):
    dir_path = settings.base_dir / 'backend' / 'apps' / app_name
    if dir_path.exists():
        raise ValueError(f"目录：{dir_path} 已经存在！")
    dir_path.mkdir(parents=True)
    return dir_path


def check_values(values: List[str]):
    for v in values:
        if re.match(r"^\d", v):
            raise ValueError(f"输入的名称不能以数字开头，{v}")
        if ' ' in v or '\t' in v:
            raise ValueError(f"输入的名称不能包含空格或者TAB,{v}")


@app.command(name='app', help='start a new app')
def start_app():
    app_name: str = prompt("请输入 App 的名字，请使用小写下划线命名")
    dir_path = check_dir(app_name)
    secho(f"您输入的APP名称为: {app_name}", fg=GREEN)
    model_name: str = prompt(
            "请使用大驼峰命名法给你的模型起一个名字\n此名称用于生成 Model 及 schema \n请输入模型的名字",
            default=app_name.title())
    secho(f"您输入的模型名称为: {model_name}", fg=GREEN)
    model_name_lower: str = prompt(
            "请使用小写下划线命名法给你的模型起一个小写名字\n此名称用于生成 接口url \n请输入模型的小写名字",
            default=app_name.lower())
    secho(f"您输入的模型小写名称为: {model_name_lower}", fg=GREEN)
    check_values([app_name, model_name, model_name_lower])

    env = Environment(loader=PackageLoader('backend.templates', 'start_app'))
    tpl_list = ['__init__.py.tpl',
                'dependencies.py.tpl',
                'models.py.tpl',
                'routers.py.tpl',
                'schemas.py.tpl',
                'test_item.py.tpl']
    for tpl in tpl_list:
        template = env.get_template(tpl)
        py_file_name = '.'.join(tpl.split('.')[:-1])
        context = {
            "time_now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "author": "my_name",
            "email": "abc@xyz.com",
            "file_name": py_file_name,
            "project": f"{settings.project_title}-{settings.project_version}",
            "app_name": app_name,
            "model_name": model_name,
            "model_name_lower": model_name_lower
            }
        py_code_str = template.render(context)
        py_file_path = dir_path / py_file_name
        py_file_path.write_text(py_code_str, encoding='utf8')

    secho("-" * 80, fg=RED)
    secho(f"已经为您自动生成了 APP ：{app_name} \n为了让新生成的APP生效，你还需要进行如下做：", fg=GREEN)
    secho("1。请在 backend/apps/__init__.py 文件中注册模型及路由", fg=GREEN)
