# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 9:30
@Auth ： 大雄
@File ：window.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import win32gui
import win32ui
import win32con
import cv2,numpy as np

from PyDmGame.modular import cutOut


class Display_gdi:
    # 后台截图
    @staticmethod
    def windows_capture(hwnd):
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

    # 截图
    def capture(self, x1=None, y1=None, x2=None, y2=None, file=None):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param file: 保存文件路径，不填写则写入cv图像到属性self._img
        :return:
        """
        # 截取并写入
        self._img = self.windows_capture(self.hwnd)
        self._img = cutOut(self._img,x1, y1, x2, y2)
        if not self._img is None:
            if file:
                cv2.imwrite(file, self._img)
            return 1
        return 0


    def getCVImg(self):
        return self._img