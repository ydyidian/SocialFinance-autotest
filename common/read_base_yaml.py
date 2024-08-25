#!/usr/bin/env python
# encoding: utf-8
import os
from common.common_base import load_yaml_data
import yaml_data

base_path = yaml_data.__path__[0]


class BaseData(object):
    """基础配置信息"""

    def __init__(self):
        self.base_info = load_yaml_data(base_path, 'login.yaml')


if __name__ == '__main__':
    base_data = BaseData()
    print(base_data.base_info)
