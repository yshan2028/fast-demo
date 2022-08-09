#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 22:11
# Author:  rongli
# Email:   abc@xyz.com
# File:    send_email.py
# Project: fa-demo
# IDE:     PyCharm
import asyncio


async def send_email(account, captcha):
    # todo 发送电子邮件
    await asyncio.sleep(3)
    print(account, '-->', captcha)
    return
