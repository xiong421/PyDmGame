# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 15:47
@Auth ： 大雄
@File ：windows.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

import win32api
import win32con

from PyDmGame.modular.vk_code import vk_to_char


class KM_windows:
    def __init__(self):
        self.setKeypadDelay()
        self.setMouseDelay()
        self.x = 0
        self.y = 0

    # 键盘 ===========================
    def setKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.01 if delay is None else delay / 1000

    def keyDownChar(self, key_str):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, vk_to_char(key_str), 0)

    def keyUpChar(self, key_str):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, vk_to_char(key_str), 0xC01E0001)

    def keyPressChar(self, key_str: str):
        self.keyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.keyUpChar(key_str)

    # def enableRealKeypad(self, enable):
    #     pass

    def sendString(self, hwnd, str_):
        for ch in str_:
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(ch), 0)
            time.sleep(self.keyboard_delay)

    # 鼠标 ===================================
    def leftDown(self):
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))  # 鼠标按下

    def leftUp(self):
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))  # 鼠标按下

    def leftClick(self):
        self.leftDown()
        time.sleep(self.mouse_delay)
        self.leftUp()

    def leftDoubleClick(self):
        self.leftClick()
        time.sleep(self.mouse_delay)
        self.leftClick()

    def rightDown(self):
        win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def rightUp(self):
        win32api.SendMessage(self.hwnd, win32con.WM_RBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def rightClick(self):
        self.rightDown()
        time.sleep(self.mouse_delay)
        self.rightUp()

    def setMouseDelay(self, delay=None):
        self.mouse_delay = 0.03 if delay is None else delay / 1000

    def middleDown(self):
        win32api.SendMessage(self.hwnd, win32con.WM_MBUTTONDOWN, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def middleUp(self):
        win32api.SendMessage(self.hwnd, win32con.WM_MBUTTONUP, win32con.MK_LBUTTON,
                             win32api.MAKELONG(self.x, self.y))

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def wheelDown(self):
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL, win32con.WHEEL_DELTA * -1,
                             win32api.MAKELONG(self.x, self.y))

    def wheelUp(self):
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL, win32con.WHEEL_DELTA * 1,
                             win32api.MAKELONG(self.x, self.y))

    def hotKey(self, key_list, interval=None):
        if not interval:
            interval = self.keyboard_delay
        for key in key_list:
            self.keyDownChar(key)
            time.sleep(interval)
        for key in key_list[::-1]:
            self.keyUpChar(key)
            time.sleep(interval)

    # def keyPressStr(self, key_list, interval=None):
    #     """
    #     支持两种格式，一种是"a,b,c",一种是["a","b","c"],或("a","b","c")等可迭代对象
    #     :param key_list:
    #     :return:
    #     """
    #     if not interval:
    #         interval = self.mouse_delay
    #     if isinstance(key_list, str):
    #         for key in key_list.split(","):
    #             self.keyPressChar(key)
    #             time.sleep(interval)
    #     else:
    #         for key in key_list:
    #             self.keyPressChar(key)
    #             time.sleep(interval)

    # def enableRealMouse(self, enable, mousedelay, mousestep):
    #     pass
