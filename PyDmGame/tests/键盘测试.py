# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 19:45
@Auth ： 大雄
@File ：键盘测试.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time
from PyDmGame import *

def normal_keyboard(hwnd):
    dm = DM()
    dm.BindWindow(hwnd, "normal", "normal", "normal", 0)
    s = time.time()
    dm.KeyPressChar("x")
    # time.sleep(1)
    # dm.KeyPressChar("right")
    # time.sleep(1)
    # dm.KeyPressChar("up")
    # time.sleep(1)
    # dm.KeyPressChar("down")
    time.sleep(1)
    print(f"耗时:{time.time() - s}")


def windows_keyboard(hwnd):
    dm = DM()
    dm.BindWindow(hwnd, "windows", "windows", "windows", 0)
    s = time.time()
    dm.KeyPressStr("1", 50)
    # dm.KeyPressChar("a")
    print(f"耗时:{time.time() - s}")


def sendstring_keyboard(hwnd):
    dm = DM()
    dm.BindWindow(hwnd, "windows", "windows", "windows", 0)
    dm.SendString(hwnd, "我是大雄")


if __name__ == '__main__':
    hwnd = 264426
    # # 测试按键输入-前台
    time.sleep(3)
    normal_keyboard(hwnd)

    # 测试按键输入-后台
    # windows_keyboard(hwnd)

    # # 测试后台输入字符串
    # sendstring_keyboard(hwnd)
