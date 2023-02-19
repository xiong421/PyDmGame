# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 21:00
@Auth ： 大雄
@File ：mouse_.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import time

from PyDmGame.modular import raise_dm_error


class Mouse:
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')

    def GetCursorPos(self,x,y):
        class POINT(ctypes.Structure):
            _fields_ = [
                ("x",ctypes.wintypes.LONG),
                ("y",ctypes.wintypes.LONG)
            ]
        point = POINT()
        self.winuser32.GetCursorPos(ctypes.byref(point))
        return (point.x,point.y)

    def GetCursorShape(self):
        class POINT(ctypes.Structure):
            _fields_ = [
                ("x",ctypes.wintypes.LONG),
                ("y",ctypes.wintypes.LONG)
            ]
        hCursor = None
        point = POINT()
        self.winuser32.GetCursorPos(ctypes.byref(point))
        hwnd = self.winuser32.WindowFromPoint(point)
        dwThreadID = self.winuser32.GetWindowThreadProcessId(hwnd, 0)
        dwCurrentThreadID = self.winKernel32.GetCurrentThreadId()
        if dwCurrentThreadID != dwThreadID:
            if self.winuser32.AttachThreadInput(dwCurrentThreadID, dwThreadID, True):
                hCursor = self.winuser32.GetCursor()
                self.winuser32.AttachThreadInput(dwCurrentThreadID, dwThreadID, False)
        else:
            hCursor = self.winuser32.GetCursor()
        return hCursor

    def LeftDown(self):
        pass

    def LeftUp(self):
        pass

    def LeftClick(self):
        pass

    def LeftDoubleClick(self):
        pass

    def RightDown(self):
        pass

    def RightUp(self):
        pass

    def RightClick(self):
        pass

    def SetMouseDelay(self,type,delay):
        pass

    @staticmethod
    def MoveTo(x,y):
        pass

    def WheelDown(self):
        pass

    def WheelUp(self):
        pass