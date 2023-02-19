# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/18 22:11
@Auth ： 大雄
@File ：yijianshu.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
class Keyboard_YJS:
    def __init__(self):
        self.SetKeypadDelay()

    def SetKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.03 if delay is None else delay / 1000

    @staticmethod
    def KeyDownChar(key_str):
        pass

    @staticmethod
    def KeyUpChar(key_str):
        pass

    def KeyPressChar(self, key_str:str):
        pass