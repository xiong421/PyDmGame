# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 23:20
@Auth ： 大雄
@File ：normal.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import time

from PyDmGame.modular import pydirectinput


class Mouse_normal:
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')

    def __init__(self):
        self.SetMouseDelay()

    @staticmethod
    def LeftDown():
        pydirectinput.mouseDown(_pause=False)

    @staticmethod
    def LeftUp():
        pydirectinput.mouseUp(_pause=False)

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
        pydirectinput.mouseDown(button="right",_pause=False)

    @staticmethod
    def RightUp():
        pydirectinput.mouseUp(button="right", _pause=False)

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
        pydirectinput.mouseDown(button="middle", _pause=False)

    @staticmethod
    def MiddleUp():
        pydirectinput.mouseUp(button="middle",_pause=False)

    @staticmethod
    def MoveTo(x,y):
        pydirectinput.moveTo(x,y)

    @staticmethod
    def WheelDown():
        pydirectinput.mouseDown(button="wheel",_pause=False)

    @staticmethod
    def WheelUp():
        pydirectinput.mouseUp(button="wheel",_pause=False)