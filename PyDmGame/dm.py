# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/6 15:44
@Auth ： 大雄
@File ：dm.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:找图找色
"""

from PyDmGame.modular import *
from PyDmGame.model.model import dmtd_info, thread_max_num


class ABC:
    pass


def createDm(hwnd="deskTop", display="normal", km="normal", ocr="ppcor"):
    if hwnd == "deskTop":
        hwnd = Window.getSpecialWindow(0)

    if display == "normal":
        displayClass = Display_normal
    elif display == "gdi":
        displayClass = Display_gdi
    elif display == "ld":
        displayClass = Display_ld
    else:
        raise "display Wrong binding mode"

    if km == "normal":
        KMClass = KM_normal
    elif km == "normal2":
        KMClass = KM_normal2
    elif km == "windows":
        KMClass = KM_windows
    elif km == "windows2":
        KMClass = KM_windows2
    elif km == "yjs":
        KMClass = KM_yjs
    elif km == "ld":
        KMClass = KM_ld
    else:
        raise "KM Wrong binding mode"

    if ocr == "ppcor":
        OCRClass = Ocr_normal
    else:
        OCRClass = ABC

    class DM(BasicSettings, displayClass, KMClass, OCRClass, PicColor):
        count = 0

        def __init__(self):
            self.__init_count()
            self.hwnd = hwnd
            self._img = None
            super(DM, self).__init__()

        def __del__(self):
            dmtd_info[self.id].clear()

        def __init_count(self):
            if self.count < thread_max_num:
                self.id = self.count
                self.count += 1
            else:
                raise f"线程不能超过{thread_max_num}个"

    return DM()


def createNomalDm(hwnd):
    displayClass = Display_normal
    KMClass = KM_normal
    OCRClass = Ocr_normal

    class DM(BasicSettings, displayClass, KMClass, OCRClass, PicColor):
        count = 0

        def __init__(self):
            self.__init_count()
            self.hwnd = hwnd
            self._img = None
            super(DM, self).__init__()

        def __del__(self):
            dmtd_info[self.id].clear()

        def __init_count(self):
            if self.count < thread_max_num:
                self.id = self.count
                self.count += 1
            else:
                raise f"线程不能超过{thread_max_num}个"

    return DM()


def createGdiDm(hwnd):
    displayClass = Display_gdi
    KMClass = KM_windows
    OCRClass = Ocr_normal

    class DM(BasicSettings, displayClass, KMClass, OCRClass, PicColor):
        count = 0

        def __init__(self):
            self.__init_count()
            self.hwnd = hwnd
            self._img = None
            super(DM, self).__init__()

        def __del__(self):
            dmtd_info[self.id].clear()

        def __init_count(self):
            if self.count < thread_max_num:
                self.id = self.count
                self.count += 1
            else:
                raise f"线程不能超过{thread_max_num}个"

    return DM()


def createLdDm():
    displayClass = Display_ld
    KMClass = KM_ld
    OCRClass = Ocr_normal

    class DM(BasicSettings, displayClass, KMClass, Ocr_normal, PicColor):
        count = 0

        def __init__(self):
            self.__init_count()
            self._img = None
            super(DM, self).__init__()

        def __del__(self):
            dmtd_info[self.id].clear()

        def __init_count(self):
            if self.count < thread_max_num:
                self.id = self.count
                self.count += 1
            else:
                raise f"线程不能超过{thread_max_num}个"

    return DM()
