# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:49
@Auth ： 大雄
@File ：backgroundSettings.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
from PyDmGame.modular.keyboard_ import *
from PyDmGame.modular.mouse_ import *
from PyDmGame.modular.display_ import *
from PyDmGame.model.model import td_info

class BackgroundSettings:
    def BindWindow(self, hwnd, display, mouse, keypad, mode=0):

        if display == "normal":
            td_info[self.id].display = Display_normal(hwnd)

        elif display == "gdi":
            td_info[self.id].display = Display_GDI(hwnd)

        else:
            raise "display绑定模式有误"

        if mouse == "normal":
            td_info[self.id].mouse = Mouse_normal()  # 没写完

        elif mouse == "windows":
            td_info[self.id].mouse = Mouse_windows(hwnd)  # 没写完

        elif mouse == "windows2":
            td_info[self.id].mouse = Mouse_windows2(hwnd)  # 没写完

        else:
            raise "mousedisplay绑定模式有误"

        if keypad == "normal":
            td_info[self.id].keypad = Keyboard_normal()

        elif keypad == "normal2":
            td_info[self.id].keypad = Keyboard_normal2()

        elif keypad == "windows":
            td_info[self.id].keypad = Keyboard_windows(hwnd)

        elif keypad == "windows2":
            td_info[self.id].keypad = Keyboard_windows2(hwnd)

        else:
            raise "keypad绑定模式有误"
