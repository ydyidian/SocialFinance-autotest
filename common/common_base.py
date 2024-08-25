#!/usr/bin/env python
# encoding: utf-8

import json
import os
import sys
from pathlib import Path

import allure
import yaml
from requests import Response

def load_yaml_data(path, file):
    """
    在指定路径path下查找文件file
    :param path: 路径
    :param file: 文件
    :return: yaml文件内容
    """

    if 'win32' in sys.platform:
        separator = "\\"
    else:
        separator = '/'
    file = Path(path + separator + file)
    print(file)
    if file.exists():
        with open(os.path.join(path, file), "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config
    else:
        raise FileExistsError


def assert_full(resp, api_conf, field='expect_result'):
    """
    输出接口返回，并进行接口校验
    :param resp: 接口响应
    :param api_conf:  接口比对配置
    :param field: 对比字段
    :return:
    """
    allure.attach("响应状态码 {}".format(resp.status_code), "")
    custom_assert(resp, api_conf, field)


def custom_assert(resp, api, field='expect_result'):
    """
    接口响应校验，非关键数据信息（基础数据校验）
    :param resp:    接口响应
    :param api:     接口请求信息
    :param field:  待匹配字段
    :return:
    """

    assert isinstance(resp, Response)
    compare_field('status_code', api['expect_result']['status_code'], resp.status_code)
    compare_field('respCode', api[field]['respCode'], json.loads(resp.text)['respCode'])
    compare_field('respMsg', api[field]['respMsg'], json.loads(resp.text)['respMsg'])


def compare_field(field_name, src, dst):
    if isinstance(dst, str) or isinstance(dst, int):
        try:
            assert str(src) == str(dst)
            allure.attach("一致性校验 {}: {} 等于 {}".format(field_name, str(src), str(dst)), "")
        except Exception:
            allure.attach("比对错误字段 {}: {} 不等于 {}".format(field_name, str(src), str(dst)), "")
            raise ValueError("比对错误字段 {}: {} 不等于 {}".format(field_name, str(src), str(dst)))
    if isinstance(dst, list):
        try:
            assert str(src) in [str(i) for i in dst]
            allure.attach("一致性校验 {}: {} 包含于 {} 内".format(field_name, str(src), str(dst)), "")
        except Exception:
            allure.attach("比对错误字段 {}: {} 不包含在 {}内".format(field_name, str(src), str(dst)), "")
            raise ValueError("比对错误字段 {}: {} 不包含在 {}".format(field_name, str(src), str(dst)))
    if isinstance(dst, bool):
        assert src == dst


def replace_dict_data(s1, d2):
    """
    读取 d2,s1中相同的元素，并替换d2 对应key的值
    :param s1:  源数据
    :param d2:  目标数据
    :return:
    """
    assert isinstance(s1, dict) and isinstance(d2, dict)
    for k in s1.keys():
        for m in d2.keys():
            if k == m:
                # 字符串直接替换
                if type(d2[m]) not in (list, dict, set):
                    d2[m] = s1[k]
                    break
                # 字典数据，递归替换
                elif isinstance(d2[m], dict):
                    replace_dict_data(s1[k], d2[m])
                elif isinstance(d2[m], list):
                    # 遍历字典列表参数 , 将目标数据全部替换成s1[k][0]
                    if s1[k] and len(d2[m]) == len(s1[k]):
                        for i in range(len(d2[m])):
                            if isinstance(s1[k][i], dict):
                                replace_dict_data(s1[k][i], d2[m][i])
                            else:
                                d2[m][i] = s1[k][i]
                    else:
                        d2[m] = s1[k]

    return d2


def is_dict_list(data):
    """
    字典列表
    :param data:
    :return:
    """
    assert isinstance(data, list)
    try:
        for i in data:
            assert isinstance(i, dict)
        return True
    except AssertionError:
        return False


def is_pure_list(data):
    """
    纯净列表，无嵌套其他的数据类型( tuple,list,dict,set等)
    :param data:
    :return:
    """
    assert isinstance(data, list)
    for i in data:
        if type(i) not in [list, tuple, dict, set]:
            return True
        else:
            return False
