# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 15:48
@Auth ： 大雄
@File ：ld.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@lnk : http://bbs.ldmnq.com/forum.php?mod=viewthread&tid=30
@func:功能
"""

import os
import random
import time

from PyDmGame.modular.basic.ld import Dnconsole


class KM_ld(Dnconsole):
    def __init__(self):
        self.setMouseDelay()
        self.enableRealMouse()

    def keyPressStr(self, key_str):
        """
        :param key_str: 字符串: 需要按下的字符串序列. 比如"1234","abcd","7389,1462"等.
        :return:
        """
        cmd = self.console + 'action --_index %d --key call.input --value %s' % (self._index, key_str)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 鼠标 ==============================================================================================================
    def leftClick(self):
        if self.mouse_delay == 0:
            self.dnld('input tap %d %d' % (self.x, self.y))
        else:
            self.dnld('input touch %d %d %d' % (self.x, self.y, self.__randomMouseDelay()))

    def setMouseDelay(self, delay=None):
        self.mouse_delay = 0.03 if delay is None else delay / 1000

    def moveTo(self, x, y):
        self.x, self.y = x, y

    # 开启点击随机延迟
    def enableRealMouse(self, mousedelay=0):
        self.random_mousedelay = mousedelay

    # 随机延迟时间
    def __randomMouseDelay(self):
        return self.mouse_delay * (random.uniform((1 - self.random_mousedelay), 1 + self.random_mousedelay))

    # 滑动
    def swipe(self, x1, y1, x2, y2, delay: int = 0):
        if delay == 0:
            self.dnld('input swipe %d %d %d %d' % (x1, y1, x2, y2))
        else:
            self.dnld('input swipe %d %d %d %d %d' % (x1, y1, x2, y2, delay))

