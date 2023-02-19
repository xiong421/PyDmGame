# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 23:20
@Auth ： 大雄
@File ：normal2.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import time

import win32api
import win32con


class Mouse_normal2:
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')

    def __init__(self):
        self.SetMouseDelay()

    @staticmethod
    def LeftDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    @staticmethod
    def LeftUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def LeftClick(self):
        self.LeftDown()
        time.sleep(self.mouse_delay)
        self.LeftUp()

    def LeftDoubleClick(self):
        self.LeftClick()
        time.sleep(self.mouse_delay)
        self.LeftClick()

    @staticmethod
    def RightDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)

    @staticmethod
    def RightUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    def RightClick(self):
        self.RightDown()
        time.sleep(self.mouse_delay)
        self.RightUp()

    def SetMouseDelay(self,delay=None):
        self.mouse_delay = 0.03 if delay is None else delay/1000

    def MiddleClick(self):
        self.MiddleDown()
        time.sleep(self.mouse_delay)
        self.MiddleUp()

    @staticmethod
    def MiddleDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)

    @staticmethod
    def MiddleUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)

    @staticmethod
    def MoveTo(x,y) -> None:
        MOUSEEVENTF_MOVE = 0x0001
        MOUSEEVENTF_ABSOLUTE  = 0x8000
        SM_CXSCREEN = 0
        SM_CYSCREEN = 1
        cx_screen = Mouse_normal2.winuser32.GetSystemMetrics(SM_CXSCREEN)
        cy_screen = Mouse_normal2.winuser32.GetSystemMetrics(SM_CYSCREEN)
        real_x = round(65535 * x / cx_screen)
        real_y = round(65535 * y / cy_screen)
        Mouse_normal2.winuser32.mouse_event(MOUSEEVENTF_ABSOLUTE|MOUSEEVENTF_MOVE,real_x,real_y,0,0)

    @staticmethod
    def WheelDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, -120, 0)

    @staticmethod
    def WheelUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 120, 0)