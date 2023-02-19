# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 20:57
@Auth ： 大雄
@File ：鼠标测试.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

from PyDmGame import *
def mouse_normal():
    dm = DM()
    dm.MoveTo(100,100)
    dm.LeftClick()
    time.sleep(1)
    dm.RightClick()
    time.sleep(1)
    dm.MoveTo(50,100)
    dm.LeftClick()
    dm.WheelDown()
    time.sleep(1)
    dm.WheelUp()

def mouse_windows(hwnd):
    dm = DM()
    dm.BindWindow(hwnd,"windows","windows","windows")
    dm.MoveTo(89,188)
    dm.LeftClick()
    time.sleep(1)
    dm.MoveTo(200,300)
    dm.LeftClick()



if __name__ == '__main__':
    # # 前台测试
    # time.sleep(1)
    # mouse_normal()

    # 后台测试
    time.sleep(2)
    hwnd = 198944
    mouse_windows(hwnd)

