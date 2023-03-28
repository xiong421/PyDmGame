# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:53
@Auth ： 大雄
@File ：basicSettings.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os


class BasicSettings:
    def __init__(self):
        self.set_find_image_path(os.getcwd())
    # 设置路径
    def set_find_image_path(self, path):
        self.path = path