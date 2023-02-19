# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:15
@Auth ： 大雄
@File ：keyboard.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time
import win32api
import win32con

class Keyboard:

    def SetKeypadDelay(self, delay=None):
        pass

    def KeyDownChar(self, key_str):
        pass

    def KeyUpChar(self, key_str):
        pass

    def KeyPressChar(self, key_str:str):
        """
        :param key_str:字符串: 字符串描述的键码. 大小写无所谓
        :return:
        """
        pass

    def KeyPressStr(self,key_str:str,delay:int):
        """
        :param key_str: 字符串: 需要按下的字符串序列. 比如"1234","abcd","7389,1462"等.
        :param delay:整形数: 每按下一个按键，需要延时多久. 单位毫秒.这个值越大，按的速度越慢。
        :return:
        """
        for key in key_str:
            self.KeyPressChar(key)
            time.sleep(delay/1000)

    def SendString(self,hwnd,str):
        for ch in str:
            win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(ch), 0)
            time.sleep(self.keyboard_delay)

