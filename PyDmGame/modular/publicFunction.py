# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:18
@Auth ： 大雄
@File ：publicFunction.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time


# 测试耗时
def test_run_time(func):
    def inner(*args, **kwargs):
        t_start = time.time()
        res = func(*args, **kwargs)
        t_end = time.time()
        print(f"一共花费了{t_end - t_start}秒时间,函数运行结果是 {res}")
        return res

    return inner


# 判断字符串是否为中文
def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def raise_dm_error(name,description):
    error = f"报错类型:{name},报错描述:{description}"
    raise error