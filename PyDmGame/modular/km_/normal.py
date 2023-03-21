# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 15:47
@Auth ： 大雄
@File ：normal.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import time

import win32gui

from PyDmGame.modular import pydirectinput


class KM_normal:
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')
    def __init__(self):
        self.setKeypadDelay()
        self.setMouseDelay()
        self.x,self.y =  win32gui.GetClientRect(self.hwnd)[:2]
    # 键盘==============================
    def setKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.03 if delay is None else delay / 1000

    @staticmethod
    def keyDownChar(key_str):
        pydirectinput.keyDown(key_str,_pause=False)

    @staticmethod
    def keyUpChar(key_str):
        pydirectinput.keyUp(key_str,_pause=False)

    def keyPressChar(self, key_str:str):
        self.keyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.keyUpChar(key_str)

    def enableRealKeypad(self,enable):
        pass

    # 鼠标==============================
    @staticmethod
    def leftDown():
        pydirectinput.mouseDown(_pause=False)

    @staticmethod
    def leftUp():
        pydirectinput.mouseUp(_pause=False)

    def leftClick(self):
        self.leftDown()
        time.sleep(self.mouse_delay)
        self.leftUp()

    def leftDoubleClick(self):
        self.leftClick()
        time.sleep(self.mouse_delay)
        self.leftClick()

    @staticmethod
    def rightDown():
        pydirectinput.mouseDown(button="right",_pause=False)

    @staticmethod
    def rightUp():
        pydirectinput.mouseUp(button="right", _pause=False)

    def rightClick(self):
        self.rightDown()
        time.sleep(self.mouse_delay)
        self.rightUp()

    def setMouseDelay(self,delay=None):
        self.mouse_delay = 0.03 if delay is None else delay/1000

    def middleClick(self):
        self.middleDown()
        time.sleep(self.mouse_delay)
        self.middleUp()

    @staticmethod
    def middleDown():
        pydirectinput.mouseDown(button="middle", _pause=False)

    @staticmethod
    def middleUp():
        pydirectinput.mouseUp(button="middle",_pause=False)

    def moveTo(self,x,y):
        pydirectinput.moveTo(self.x + x,self.y+y)

    @staticmethod
    def wheelDown():
        pydirectinput.mouseDown(button="wheel",_pause=False)

    @staticmethod
    def wheelUp():
        pydirectinput.mouseUp(button="wheel",_pause=False)

    # def enableRealMouse(self,enable,mousedelay,mousestep):
    #     pass