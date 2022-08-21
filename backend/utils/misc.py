#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-28 22:14
# Author:  rongli
# Email:   abc@xyz.com
# File:    captcha.py
# Project: fa-demo
# IDE:     PyCharm
from typing import List


def make_tree(data, parent_id=0, parent_key='parent_id', key_key='key') -> List[dict]:
    """
    生成的树结构
    :param data: 需要处理的数据
    :param parent_id: 父节点的唯一属性
    :param parent_key: 用来标注父节点的唯一属性的 key
    :param key_key: 节点的 key 值，用来标注当前节点的唯一属性
    :return: 树结构的字典
    """
    result = []
    for item in data:
        if parent_id == item[parent_key]:
            temp = make_tree(data, item[key_key], parent_key, key_key)
            if len(temp) > 0:
                item["children"] = temp
            result.append(item)
    return result
