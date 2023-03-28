# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 15:52
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
import win32gui

from PyDmGame.modular.vk_code import vk_to_char


class KM_normal2:
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')

    def __init__(self):
        self.setKeypadDelay()
        self.setMouseDelay()
        self.setMouseDelay()
        self.x, self.y = win32gui.GetClientRect(self.hwnd)[:2]

    # 键盘 ==========================
    def setKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.03 if delay is None else delay / 1000

    @staticmethod
    def keyDownChar(key_str):
        win32api.keybd_event(vk_to_char(key_str), 0, 0, 0)

    @staticmethod
    def keyUpChar(key_str):
        win32api.keybd_event(vk_to_char(key_str), 0, 2, 0)

    def keyPressChar(self, key_str: str):
        self.keyDownChar(key_str)
        time.sleep(self.keyboard_delay)
        self.keyUpChar(key_str)

    # def enableRealKeypad(self, enable):
    #     pass

    # 鼠标 ==================================

    @staticmethod
    def leftDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    @staticmethod
    def leftUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

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
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)

    @staticmethod
    def rightUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    def rightClick(self):
        self.rightDown()
        time.sleep(self.mouse_delay)
        self.rightUp()

    def setMouseDelay(self, delay=None):
        self.mouse_delay = 0.03 if delay is None else delay / 1000

    def middleClick(self):
        self.middleDown()
        time.sleep(self.mouse_delay)
        self.middleUp()

    @staticmethod
    def middleDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0)

    @staticmethod
    def middleUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0)

    def moveTo(self, x, y) -> None:
        MOUSEEVENTF_MOVE = 0x0001
        MOUSEEVENTF_ABSOLUTE = 0x8000
        SM_CXSCREEN = 0
        SM_CYSCREEN = 1
        cx_screen = self.winuser32.GetSystemMetrics(SM_CXSCREEN)
        cy_screen = self.winuser32.GetSystemMetrics(SM_CYSCREEN)
        real_x = round(65535 * (self.x + x) / cx_screen)
        real_y = round(65535 * (self.y + y) / cy_screen)
        self.winuser32.mouse_event(MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, real_x, real_y, 0, 0)

    @staticmethod
    def wheelDown():
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, -120, 0)

    @staticmethod
    def wheelUp():
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 120, 0)

    def hotKey(self, key_list, interval=None):
        if not interval:
            interval = self.mouse_delay
        for key in key_list:
            self.keyDownChar(key)
            time.sleep(interval)
        for key in key_list[::-1]:
            self.keyUpChar(key)
            time.sleep(interval)

    def keyPressStr(self, key_list, interval=None):
        """
        支持两种格式，一种是"a,b,c",一种是["a","b","c"],或("a","b","c")等可迭代对象
        :param key_list:
        :return:
        """
        if not interval:
            interval = self.keyboard_delay
        if isinstance(key_list, str):
            for key in key_list.split(","):
                self.keyPressChar(key)
                time.sleep(interval)
        else:
            for key in key_list:
                self.keyPressChar(key)
                time.sleep(interval)
    # def EnableRealMouse(self,enable,mousedelay,mousestep):
    #     pass
