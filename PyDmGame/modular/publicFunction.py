# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:18
@Auth ： 大雄
@File ：publicFunction.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

# 测试耗时
import cv2, numpy as np
import win32clipboard


def test_run_time(func):
    def inner(*args, **kwargs):
        t_start = time.time()
        res = func(*args, **kwargs)
        t_end = time.time()
        print(f"一共花费了{t_end - t_start}秒时间,函数运行结果是 {res}")
        return res

    return inner


def raise_dm_error(name, description):
    error = f"报错类型:{name},报错描述:{description}"
    raise error


def ps_to_img(img, ps):
    """
    :param img: cv图像
    :param ps: 偏色
    :return: 偏色后的cv图像
    """
    # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
    if not ps:
        return img

    elif type(ps) == str:
        lower, upper = color_to_range(ps, 1)
        img = inRange(img, lower, upper)

    elif type(ps) == tuple or type(ps) == list:
        lower, upper = ps
        img_hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = inRange(img_hsv1, lower, upper)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return img


# 转换大漠格式RGB "ffffff-303030" 为 BGR遮罩范围(100,100,100),(255,255,255)
def color_to_range(color, sim):
    if sim <= 1:
        if len(color) == 6:
            c = color
            weight = "000000"
        elif "-" in color:
            c, weight = color.split("-")
        else:
            raise "参数错误"
    else:
        raise "参数错误"
    color = int(c[4:], 16), int(c[2:4], 16), int(c[:2], 16)
    weight = int(weight[4:], 16), int(weight[2:4], 16), int(weight[:2], 16)
    sim = int((1 - sim) * 255)
    lower = tuple(map(lambda c, w: max(0, c - w - sim), color, weight))
    upper = tuple(map(lambda c, w: min(c + w + sim, 255), color, weight))
    return lower, upper


def inRange(img, lower, upper):
    mask = cv2.inRange(img, np.array(lower), np.array(upper))
    img = cv2.bitwise_and(img, img, mask=mask)
    return img


def send_msg_to_clip(type_data, msg):
    """
    操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()

    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()


# 截取图像范围
def cutOut(img, x1, y1, x2, y2):
    if None in [x1, y1, x2, y2] or sum([x1, y1, x2, y2]) == 0:
        return img
    height, width = img.shape[:2]
    if y1 <= y2 <= height and x1 <= x2 <= width:
        return img[y1:y2, x1:x2]
    else:
        raise "x1,y1,x2,y2图像范围溢出"


def imgshow(img):
    windows_name = "img"
    cv2.imshow(windows_name, img)
    cv2.waitKey()
    # cv2.destroyWindow(windows_name)


def lower_upper21(lower, upper):
    """
    颜色的上限和下限，-1或者+1，避免相等
    :param lower:
    :param upper:
    :return:
    """
    new_lower, new_upper = [], []
    for down, up in zip(lower, upper):
        if down == up > 0:
            down -= 1
        elif down == up == 0:
            up += 1
        new_lower.append(down)
        new_upper.append(up)
    return new_lower, new_upper
