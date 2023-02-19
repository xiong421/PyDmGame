# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:21
@Auth ： 大雄
@File ：picColor.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os
from PyDmGame.modular.publicFunction import *
from functools import reduce
import cv2,numpy as np

class PicColor:

    # 随机创建图片,用于测试算法
    def create_random_img(self, width, height, item=3):
        img = np.random.randint(0, 255, (width, height, item))
        img = img.astype(np.uint8)
        return img

    # 转换大漠格式RGB "ffffff-303030" 为 BGR遮罩范围(100,100,100),(255,255,255)
    def __color_to_range(self, color, sim):
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

    def __imread(self, path):
        # 读取图片
        if is_chinese(path):
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)  # 避免路径有中文
        else:
            img = cv2.imread(path)
        return img

    def __inRange(self, img, lower, upper):
        mask = cv2.inRange(img, np.array(lower), np.array(upper))
        img = cv2.bitwise_and(img, img, mask=mask)
        return img

    def __imgshow(self, img):
        windows_name = "img"
        cv2.imshow(windows_name, img)
        cv2.waitKey()
        cv2.destroyWindow(windows_name)

    def __ps_to_img(self, img, ps):
        """
        :param img: cv图像
        :param ps: 偏色
        :return: 偏色后的cv图像
        """
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        if not ps:
            return img

        elif type(ps) == str:
            lower, upper = self.__color_to_range(ps, 1)
            img = self.__inRange(img, lower, upper)

        elif type(ps) == tuple:
            lower, upper = ps
            img_hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = self.__inRange(img_hsv1, lower, upper)
        return img


    def __FindPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, method, drag=None):
        # 读取图片
        ret = self.Capture(x1, y1, x2, y2)
        if ret:
            img1 = self.GetCVImg()
        else:
            raise "截圖失敗"
        img2 = self.__imread(self.path + os.path.sep + pic_name)

        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        img1 = self.__ps_to_img(img1, delta_color)
        img2 = self.__ps_to_img(img2, delta_color)
        # 利用cv的模板匹配找图
        result = cv2.matchTemplate(img1, img2, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        yloc, xloc = np.where(result >= sim)
        height, width = img2.shape[:2]
        return result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width

    # 单点比色
    def CmpColor(self, x, y, color, sim=1):
        """
        :param x: 坐标x
        :param y: 坐标y
        :param color: 颜色字符串,可以支持偏色,"ffffff-202020",最多支持一个
        :param sim:相似度(0.1-1.0) (0,255)
        :return:bool
        """
        ret = self.Capture(0, 0, 0, 0)
        if ret:
            img = self.GetCVImg()
        else:
            raise "截圖失敗"
        lower, upper = self.__color_to_range(color, sim)
        if not lower is None:
            new_color = img[y,x]
            for i in [0, 1, 2]:
                if new_color[i] < lower[i] or new_color[i] > upper[i]:
                    return False
            return True
        return False

    # 范围找色
    def FindColor(self, x1, y1, x2, y2, color, sim, dir=None):
        ret = self.Capture(x1, y1, x2, y2)
        if ret:
            img = self.GetCVImg()
        else:
            raise "截圖失敗"
        lower, upper = self.__color_to_range(color, sim)
        height, width = img.shape[:2]
        b, g, r = cv2.split(img)
        b = b.reshape(1, height * width)
        g = g.reshape(1, height * width)
        r = r.reshape(1, height * width)
        key1 = np.where(lower[0] <= b)
        key2 = np.where(lower[1] <= g)
        key3 = np.where(lower[2] <= r)
        key4 = np.where(upper[0] >= b)
        key5 = np.where(upper[1] >= g)
        key6 = np.where(upper[2] >= r)

        if len(key1[0]) and len(key2[0]) and len(key3[0]) and len(key4[0]) and len(key5[0]) and len(key6[0]):
            keys = reduce(np.intersect1d, [key1, key2, key3, key4, key5, key6])  # 相似度越小,交集数据越多,找的慢,相似度越大,找的越快,主要耗时的地方
            if len(keys):
                x, y = divmod(keys[1], width)
                return 0, x + x1, y + y1
        return -1, -1, -1

    # 找图
    def FindPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None):
        """
        :param x1:区域的左上X坐标
        :param y1:区域的左上Y坐标
        :param x2:区域的右下X坐标
        :param y2:区域的右下Y坐标
        :param pic_name:图片名，只能单个图片
        :param delta_color:偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
        :param sim:相似度，和算法相关
        :param dir:仿大漠，总共有6总
        :param drag:是否在找到的位置画图并显示,默认不画
               方差匹配方法：匹配度越高，值越接近于0。
               归一化方差匹配方法：完全匹配结果为0。
               相关性匹配方法：完全匹配会得到很大值，不匹配会得到一个很小值或0。
               归一化的互相关匹配方法：完全匹配会得到1， 完全不匹配会得到0。
               相关系数匹配方法：完全匹配会得到一个很大值，完全不匹配会得到0，完全负相关会得到很大的负数。
                    （此处与书籍以及大部分分享的资料所认为不同，研究公式发现，只有归一化的相关系数才会有[-1,1]的值域）
               归一化的相关系数匹配方法：完全匹配会得到1，完全负相关匹配会得到-1，完全不匹配会得到0。
        :return:
        """
        result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width = self.__FindPic(x1, y1, x2, y2, pic_name,
                                                                                               delta_color, sim,
                                                                                               method=5, drag=None)
        if len(xloc):
            x, y = max_loc[0] + x1, max_loc[1] + y1
            if drag:
                img = cv2.rectangle(self.GetCVImg(), (x, y), (x + width, y + height), (255, 0, 0), thickness=2)
                self.__imgshow(img)
            return 0, x, y
        return -1, -1, -1

    # 找图，返回多个匹配地址
    def FindPics(self, x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None):
        result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width = self.__FindPic(x1, y1, x2, y2, pic_name,
                                                                                               delta_color, sim,
                                                                                               method=5, drag=None)
        if len(xloc):
            if drag:
                for loc in zip(xloc, yloc):
                    img = cv2.rectangle(self.GetCVImg(), (loc[0], loc[1]), (loc[0] + width, loc[1] + height), (255, 0, 0),
                                        thickness=2)
                    self.__imgshow(img)
            return 0, zip(xloc, yloc)
        return -1, [-1, -1]


    # 截图
    def Capture(self, x1, y1, x2, y2, file=None):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param file: 保存文件路径，不填写则写入cv图像到属性img
        :return:
        """
        pass

    # 获取cv图像
    def GetCVImg(self):
        pass