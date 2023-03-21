# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/21 13:22
@Auth ： 大雄
@File ：第一次使用.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

from PyDmGame import *

dm = createLdDm()
dm.set_ld_path(r"F:\LDPlayer\LDPlayer3.0\dnplayer.exe")
dm.set_ldNum(0)
dm.set_ld_temp_image(r"C:/Users/xiong/Pictures")

dm = createGdiDm(723588)

# # 截图
# dm.capture()
# img = dm.getCVImg()
# dm.imshow(img)
s = time.time()
dm.set_ocr_save(False)
res = dm.ocr(545,132,657,161,"",0.8)
print(res)
print(time.time() - s)
