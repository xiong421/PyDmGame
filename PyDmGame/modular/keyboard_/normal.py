# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 10:21
@Auth ： 大雄
@File ：normal.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time
from PyDmGame.modular.vk_code import vk_to_char
from PyDmGame.modular import pydirectinput

class Keyboard_normal():
    def __init__(self):
        self.SetKeypadDelay()

    def SetKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.03 if delay is None else delay / 1000

    @staticmethod
    def KeyDownChar(key_str):
        pydirectinput.keyDown(key_str,_pause=False)

    @staticmethod
    def KeyUpChar(key_str):
        pydirectinput.keyUp(key_str,_pause=False)

    def KeyPressChar(self, key_str:str):
        self.KeyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.KeyUpChar(key_str)


