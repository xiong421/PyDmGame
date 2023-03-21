# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 15:47
@Auth ： 大雄
@File ：yjs.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import os
import random
import struct
import time
from ctypes import wintypes

import win32con
import win32gui
import win32print

from PyDmGame.modular.vk_code import vk_to_char


class KM_yjs:
    def __init__(self):
        self.id = id
        self.obj = self.create_obj()
        try:
            self.hdl = self.obj.M_Open_VidPid(0xC216, 0x0301)  # 获取usb键鼠
            print("易建鼠创建对象成功")
        except:
            print("易建鼠默认VID,PID创建对象失败,请通过函数CreateHANDLE来创建易建鼠hdl对象")
            self.hdl = None

        self.setKeypadDelay()
        self.enableRealKeypad()
        self.setMouseDelay()
        self.enableRealMouse()
        self.x, self.y = win32gui.GetClientRect(self.hwnd)[:2]

    def __del__(self):
        try:
            self.obj.M_ReleaseAllKey(self.hdl)  # 弹起所有按键
            print("弹起所有按键")
        except Exception as e:
            print(f"删除对象之前弹起按键失败:{e}")

    def create_obj(self):
        if struct.calcsize('P') * 8 != 32:
            path_dll = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dll64/msdk.dll"))
            yjs_km_obj = ctypes.windll.LoadLibrary(path_dll)
            yjs_km_obj.M_Open_VidPid.restype = wintypes.LPHANDLE
        else:
            path_dll = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dll/32/msdk.dll"))
            yjs_km_obj = ctypes.windll.LoadLibrary(path_dll)
        return yjs_km_obj


    # 键盘 ==============================================================================================================
    # 设置新 VID/PID;
    def setNewVidPid(self, mVID, mPID, sVID=None, sPID=None):
        """
        :param mVID: 主控端VID，如果是 0，表示 mVid、mPid 不需要更改
                     单头主控端 Vid 尾数必须是 0 3 6 9 C F 中其中一个数，如 C300或 C30C
                     双头主控端 Vid 尾数必须是 1 4 7 A D 中其中一个数，如 C301或 C30A
        :param mPID: 主控端PID,不能是 0000 或 FFFF
                     不能是 C216 或 C217 或 FFFF;
        :param sVID: 被控端，如果是单头则忽略
                     如果是 0，表示 sVid、sPid 不需要更改; sPid 的值将被忽略。
                     双头被控端 Vid 尾数必须是 2 5 8 B E 中其中一个数，如 C302或 C30B
        :param sPID: 被控端，如果是单头则武略
                     如果是 0，表示 sVid、sPid 不需要更改; sPid 的值将被忽略。
                     双头被控端 Vid 尾数必须是 2 5 8 B E 中其中一个数，如 C302或 C30B
        :return:返回值说明：
                    0: 成功；
                    2：该盒子不支持修改；
                    10: mVID 不符合规则 -11: mPID 不符合规则
                    20: sVID 不符合规则 -21: sPID 不符合规则
                    其他: 修改失败
        """
        return self.obj.M_SetNewVidPid(self.hdl, mVID, mPID, sVID, sPID)

    # 创建键鼠对象,使用默认值时不需要创建
    def createHANDLE(self, VID, PID):
        self.hdl = self.obj.M_Open_VidPid(VID, PID)  # 获取usb键鼠

    # 脚本加密使用
    def setUserData(self, LenUserData, UserData):
        """
        写用户数据
        该接口仅支持可修改 VID/PID 的单双头盒子。
        使用该接口可以将脚本运行密钥等信息写入盒子中，这些信息将被加
        密压缩后存入盒子中，这些信息不可读取，只能验证。

        :param LenUserData:数据长度(单位: 字节)，不能超过 256 字节
        :param UserData:数据
        :return:0 成功
                非 0 失败
        """
        return self.obj.M_SetUserData(self.hdl, LenUserData, UserData)

    def verifyUserData(self, LenUserData, UserData):
        """
        验证用户数据
        :param LenUserData:数据长度(单位: 字节)，不能超过 256 字节
        :param UserData:数据
        :return:0 成功
                非 0 失败
        """
        return self.obj.M_SetUserData(self.hdl, LenUserData, UserData)

    def setKeypadDelay(self, delay=None):
        self.keyboard_delay = 0.05 if delay is None else delay / 1000

    def keyDownChar(self, key_str):
        self.obj.M_KeyDown2(self.hdl, vk_to_char(key_str), 1)

    def keyUpChar(self, key_str):
        self.obj.M_KeyUp2(self.hdl, vk_to_char(key_str), 1)

    def keyPressChar(self, key_str: str):
        self.keyDownChar(key_str)
        self.keyboard_delay = random.uniform(self.keyboard_delay * self.random_delay[0],
                                             self.keyboard_delay * (1 + self.random_delay[1]))
        time.sleep(self.keyboard_delay)
        self.keyUpChar(key_str)

    def enableRealKeypad(self, enable=None):
        if enable:
            if len(enable) == 2 and (type(enable) == list or type(enable) == tuple):
                self.random_delay = enable
            else:
                self.random_delay = (0.5, 1.5)
        else:
            self.random_delay = (0, 0)



    # 鼠标 =============================================================================================================
    def leftDown(self):
        self.obj.M_LeftDown(self.hdl)

    def leftUp(self):
        self.obj.M_LeftUp(self.hdl)

    def leftClick(self):
        self.leftDown()
        self.mouse_delay = random.uniform(self.mouse_delay * self.random_delay[0],
                                          self.mouse_delay * self.random_delay[1])
        time.sleep(self.mouse_delay)
        self.leftDown()

    def leftDoubleClick(self):
        self.leftClick()
        time.sleep(self.mouse_delay)
        self.leftClick()

    def rightDown(self):
        self.obj.M_RightDown(self.hdl)

    def rightUp(self):
        self.obj.M_RightUp(self.hdl)

    def rightClick(self):
        self.rightDown()
        self.mouse_delay = random.uniform(self.mouse_delay * self.random_delay[0],
                                          self.mouse_delay * self.random_delay[1])
        time.sleep(self.mouse_delay)
        self.rightUp()

    def setMouseDelay(self, delay=None):
        self.mouse_delay = 0.05 if delay is None else delay / 1000

    def middleClick(self):
        self.middleDown()
        self.mouse_delay = random.uniform(self.mouse_delay * self.random_delay[0],
                                          self.mouse_delay * self.random_delay[1])
        time.sleep(self.mouse_delay)
        self.middleUp()

    def middleDown(self):
        self.obj.M_MiddleDown(self.hdl)

    def middleUp(self):
        self.obj.M_MiddleUp(self.hdl)

    def moveTo(self, x, y):
        # 瞬间移动
        if self.move_flag == 0:
            self.obj.M_MoveTo3_D(self.hdl, self.x + x, self.y + y)

        # 模拟移动
        elif self.move_flag == 1:
            self.obj.M_MoveTo3(self.hdl, self.x + x, self.y + y)

    def wheelDown(self):
        self.obj.M_MouseWheel(self.hdl, -1)

    def wheelUp(self):
        self.obj.M_MouseWheel(self.hdl, 1)

    def enableRealMouse(self, enable=None, mousedelay=None, mousestep=None):
        """
        :param enable: 是否开启模拟轨迹
        :param mousedelay: 默认间隔10-20，无需设置
        :param mousestep: 每次移动100像素，无需设置
        :return:
        """
        if enable:
            self.move_flag = 1
        else:
            self.move_flag = 0
            hDC = win32gui.GetDC(0)
            w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)  # 横向分辨率
            h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)  # 纵向分辨率
            self.obj.M_ResolutionUsed(self.hdl,w,h)

        if mousedelay:
            self.random_delay = [0.5, 1.5]
        else:
            self.random_delay = [0, 0]
