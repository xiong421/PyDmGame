# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 11:30
@Auth ： 大雄
@File ：windows2.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

import win32api
import win32con


class Keyboard_windows2:
    def __init__(self):
        self.SetKeypadDelay()

    def SetKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.01 if delay is None else delay/1000

    def KeyDownChar(self, key_str):
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, self.GetVK_CODE(key_str), 0)

    def KeyUpChar(self, key_str):
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, self.GetVK_CODE(key_str), 0xC01E0001)

    def KeyPressChar(self, key_str:str):
        self.KeyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.KeyUpChar(key_str)
