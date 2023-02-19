# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 23:25
@Auth ： 大雄
@File ：window2.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""

import time
import win32api
import win32con

class Mouse_windows2:
    def __init__(self,hwnd):
        self.hwnd = hwnd
        self.SetMouseDelay()
        self.x = 0
        self.y = 0

    def LeftDown(self):
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(self.x,self.y)) # 鼠标按下

    def LeftUp(self):
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))  # 鼠标按下

    def LeftClick(self):
        self.LeftDown()
        time.sleep(self.mouse_delay)
        self.LeftUp()

    def LeftDoubleClick(self):
        self.LeftClick()
        time.sleep(self.mouse_delay)
        self.LeftClick()

    def RightDown(self):
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def RightUp(self):
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def RightClick(self):
        self.RightClick()
        time.sleep(self.mouse_delay)
        self.RightClick()

    def SetMouseDelay(self,delay=None):
        self.mouse_delay = 0.03 if delay is None else delay/1000

    def MiddleDown(self):
        win32api.PostMessage(self.hwnd, win32con.WM_MBUTTONDOWN, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def MiddleUp(self):
        win32api.PostMessage(self.hwnd, win32con.WM_MBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def MoveTo(self,x,y):
        self.x = x
        self.y = y
        point = win32api.MAKELONG(x, y)
        win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, None, point)

    # def WheelDown(self):
    #     pass
    #
    # def WheelUp(self):
    #     pass
