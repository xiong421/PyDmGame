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
from PyDmGame.model.model import td_info,thread_max_num

class DM(Keyboard,Mouse,BackgroundSettings,BasicSettings,Ocr,PicColor,Window):
    count = 0
    def __getattribute__(self, item):
        ret = super(Keyboard, self).__getattribute__(item)
        if str(type(ret))=="<class 'function'>" or str(type(ret))=="<class 'method'>":
            flag = [td_info[self.id].display,td_info[self.id].keyboard,td_info[self.id].mouse]
            if not None is flag:
                for i in flag:
                    if hasattr(i,ret.__name__):
                        def res(*args):
                            func = getattr(i, ret.__name__)
                            return func(*args)
                        return res
        return ret

    def __del__(self):
        td_info[self.id].clear()

    def __init__(self):
        if self.count <thread_max_num:
            self.id = self.count
            self.count += 1
        else:
            for k,obj in enumerate(td_info):
                if None is obj.mouse:
                    self.id = k
                    break
            else:
                raise f"线程不能超过{thread_max_num}个"
        td_info[self.id].display = Display_normal(Window.GetSpecialWindow(0))
        td_info[self.id].keyboard = Keyboard_normal()
        td_info[self.id].mouse = Mouse_normal()

if __name__ == '__main__':
    # dm = DM()
    # # 单点比色
    # dm.CmpColor(100, 200, "888888-505050", 0.9)
    # 范围找色
    # dm.FindColor(0, 0, 1920 - 1, 1080 - 1, "ffff00-404040", 1, 0)
    # 找图
    # dm = DM(r"E:\code\python\demo\功能\仿大漠\鼠标原图6.png")
    # dm.SetPath(r"E:\code\python\demo\功能\仿大漠")
    # print(dm.FindPic(0, 0, 960, 540, "鼠标手1.bmp", ((0, 0, 221), (180, 30, 255)), 0.9, 5, True))

    # # 测试ocr功能
    # dm = DM(r"E:\code\python\demo\功能\仿大漠\鼠标原图6.png")
    # result = dm.OcrServer(0, 0, 960, 540, '', 0.8)
    # print(result)

    # # 测试速度
    # 小图 = r"E:\code\python\demo\功能\仿大漠\小图.bmp"
    # 大图 = r"E:\code\python\demo\功能\仿大漠\鼠标原图6.png"
    # dm = DM(大图)
    # p_num = 10
    # task_num = 20
    # p = Pool(p_num)
    # s = time.time()
    # for i in range(task_num):
    #     p.apply_async(dm.OcrServer, args=(0, 0, 960, 540, "", 0.7,))
    # p.close()
    # p.join()
    # print(f"并发{p_num},总请求{task_num},总耗时{time.time() - s}")

    # 测试OcrNum
    # dm = DM(r"E:\code\python\demo\功能\仿大漠\token_test\010.bmp")
    # dm.SetPath(r"E:\code\python\demo\功能\仿大漠")
    # num = dm.OcrNum(0,0,0,0,"",0.95,"token_num")
    # print(num)

    # # 截图
    # dm = DM()
    # dm.BindWindow(657562,"window","window","window",0)
    # if dm.Capture(0,0,0,0):
    #     cv2.imshow("img",dm.img)
    #     cv2.waitKey()

    # # 后台键鼠
    # time.sleep(3)
    # dm = DM()
    # dm.BindWindow(657562, "window", "window", "window", 0)
    # dm.KeyPressChar("1")
    # dm.KeyPressStr("1234",50)

    # 前台键鼠
    time.sleep(3)
    dm = DM()
    dm.BindWindow(657562, "window", "window", "normal", 0)
    dm.KeyPressStr("1234556", 50)
