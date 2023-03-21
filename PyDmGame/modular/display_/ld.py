# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 11:44
@Auth ： 大雄
@File ：ld.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os
import time
import cv2
from PyDmGame.modular.basic.ld import Dnconsole, DnPlayer

class Display_ld(Dnconsole):

    def _windows_capture(self, index):
        img_path = f'screencap -p /sdcard/Pictures/{index}.png'
        self.dnld(img_path)
        self._img =  self.imread(self.ld_temp_image + f"\\{index}.png")
        return self._img

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
        self._img = self._windows_capture(self._index)
        self._img = self.cutOut(x1, y1, x2, y2)
        if not self._img is None:
            if file:
                cv2.imwrite(file, self._img)
            return 1
        return 0

    # 截取图像范围
    def cutOut(self, x1, y1, x2, y2):
        if None in [x1, y1, x2, y2] or sum([x1, y1, x2, y2]) == 0:
            return self._img
        height, width = self._img.shape[:2]
        if y1 <= y2 <= height and x1 <= x2 <= width:
            return self._img[y1:y2, x1:x2]
        else:
            raise "x1,y1,x2,y2图像范围溢出"

    def getCVImg(self):
        return self._img
