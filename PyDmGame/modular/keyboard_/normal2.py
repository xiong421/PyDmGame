# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 11:26
@Auth ： 大雄
@File ：normal2.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

from PyDmGame.modular.vk_code import vk_to_char
import win32api

class Keyboard_normal2:
    def __init__(self):
        self.SetKeypadDelay()

    def SetKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.03 if delay is None else delay / 1000

    @staticmethod
    def KeyDownChar(key_str):
        win32api.keybd_event(vk_to_char(key_str), 0, 0, 0)

    @staticmethod
    def KeyUpChar(key_str):
        win32api.keybd_event(vk_to_char(key_str), 0, 2, 0)

    def KeyPressChar(self, key_str:str):
        self.KeyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.KeyUpChar(key_str)

