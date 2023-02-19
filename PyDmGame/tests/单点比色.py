# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 12:28
@Auth ： 大雄
@File ：单点比色.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""

import PyDmGame

dm = PyDmGame.DM()
dm.BindWindow(68150,"gdi","windows","windows",0)
result = dm.CmpColor(199,175, "f4c51f", 0.9)
print(result)