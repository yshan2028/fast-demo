#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-08-22 00:42
# Author:  rongli
# Email:   abc@xyz.com
# File:    utils_password.py
# Project: fa-demo
# IDE:     PyCharm
from passlib.handlers.pbkdf2 import pbkdf2_sha256

"""
已废弃
改到 User 模型下
"""


def encrypt_password(raw_password: str) -> str:
    """
    加密用户密码
    :param raw_password: 明文密码
    :return: 密文密码
    """
    hash_password = pbkdf2_sha256.hash(raw_password)
    return hash_password


def verify_password(raw_password: str, hash_password: str) -> bool:
    """
    验证密码
    :param raw_password: 明文密码
    :param hash_password: 密文密码
    :return:
    """
    return pbkdf2_sha256.verify(raw_password, hash_password)
