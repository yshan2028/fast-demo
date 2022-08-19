#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 22:14
# Author:  rongli
# Email:   abc@xyz.com
# File:    captcha.py
# Project: fa-demo
# IDE:     PyCharm
import hashlib
import random
import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256


def random_num(length=6) -> str:
    """
    生成指定长度的纯数字字符串
    :param length: 长度
    :return:
    """
    return ''.join([random.choice('0123456789') for _ in range(length)])


def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)


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


def make_tree(data, parent_id=0, parent_key='parent_id', key_key='key'):
    """ 生成的树结构 """
    result = []
    for item in data:
        if parent_id == item[parent_key]:
            temp = make_tree(data, item[key_key], parent_key, key_key)
            if len(temp) > 0:
                item["children"] = temp
            result.append(item)
    return result


def save_file(file_full_path, contents):
    with open(file_full_path, 'wb') as f:
        f.write(contents)
