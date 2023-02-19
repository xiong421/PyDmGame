# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 9:30
@Auth ： 大雄
@File ：normal.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

import win32con
import win32gui
import win32ui
import cv2, numpy as np

class Display_normal:

    def __init__(self,hwnd):
        self.hwnd = hwnd
        self.img = None
        
    # 后台截图
    @staticmethod
    def __windows_capture(hwnd):
        # pip install pywin32 -i https://pypi.douban.com/simple
        # 获取窗口宽，高
        x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
        width = x2 - x
        height = y2 - y
        # 截图
        hWndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        # 保存图片转cv图像
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (height, width, 4)
        img = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
        # 释放内存
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hWndDC)
        return img

    # 截取图像范围
    def __cutOut(self, x1, y1, x2, y2):
        if sum([x1, y1, x2, y2]) == 0:
            return self.img
        height, width = self.img.shape[:2]
        if y1 <= y2 <= height and x1 <= x2 <= width:
            return self.img[y1:y2, x1:x2]
        else:
            raise "x1,y1,x2,y2图像范围溢出"
        
    # 前台截图
    def normal_capture(self):
        if win32gui.GetWindowPlacement(self.hwnd)[1] != win32con.SW_SHOWNORMAL:
            win32gui.SendMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        topHwnd = win32gui.GetForegroundWindow()
        if topHwnd != self.hwnd:
            win32gui.SetForegroundWindow(self.hwnd)

        # # 是否激活窗口,避免遮挡
        # if win32gui.GetWindowPlacement(self.hwnd)[1] != win32con.SW_SHOWNORMAL:
        #     win32gui.SendMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        #     time.sleep(0.1)
        # # 是否显示窗口
        # topHwnd = win32gui.GetForegroundWindow()
        # if topHwnd != self.hwnd:
        #     win32gui.SetForegroundWindow(self.hwnd)
        #     time.sleep(0.3)
        # 截图
        desk_hwnd = win32gui.GetDesktopWindow()
        img = self.__windows_capture(desk_hwnd)
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.hwnd)
        img = img[y1:y2, x1:x2]
        return img

    # 截图
    def Capture(self, x1, y1, x2, y2, file=None):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param file: 保存文件路径，不填写则写入cv图像到属性self.img
        :return:
        """
        # 截取并写入
        self.img = self.normal_capture()
        self.img = self.__cutOut(x1, y1, x2, y2)
        if not self.img is None:
            if file:
                cv2.imwrite(file, self.img)
            return 1
        return 0

    def GetCVImg(self):
        return self.img
