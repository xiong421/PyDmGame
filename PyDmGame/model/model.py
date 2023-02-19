# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/18 16:22
@Auth ： 大雄
@File ：model.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import threading

thread_max_num = 1000
class Custom:
    def __init__(self):
        self.display = None
        self.mouse = None
        self.keyboard = None
    def clear(self):
        self.__init__()
def tdi():
    re = []
    for i in range(thread_max_num):
        re.append(Custom())
    return re
td_info = tdi()
