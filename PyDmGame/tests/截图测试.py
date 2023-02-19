# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 16:48
@Auth ： 大雄
@File ：截图测试.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

import cv2
from PyDmGame import *

def normal_capture(hwnd):
    dm = DM()
    dm.BindWindow(hwnd,"normal","normal","windows",0)
    # 置顶窗口
    dm.SetWindowState(hwnd,7)
    time.sleep(1)
    s = time.time()
    ret = dm.Capture(0,0,0,0)
    if ret:
        print(f"耗时:{time.time()-s}")
        cv2.imshow("img",dm.GetCVImg())
        cv2.waitKey()

def windows_capture(hwnd):
    dm = DM()
    dm.BindWindow(hwnd,"normal","windows","windows",0)
    s = time.time()
    ret = dm.Capture(0,0,0,0)
    if ret:
        print(f"耗时:{time.time()-s}")
        cv2.imshow("img",dm.GetCVImg())
        cv2.waitKey()

if __name__ == '__main__':
    # 前台截图,请自行修改句柄hwnd
    # time.sleep(5)
    hwnd = 198944
    # normal_capture(hwnd)
    # 后台截图
    windows_capture(hwnd)