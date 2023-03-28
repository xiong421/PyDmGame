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
import cv2, numpy as np


class PicColor:
    # 随机创建图片,用于测试算法
    @staticmethod
    def _create_random_img(width, height, item=3):
        img = np.random.randint(0, 255, (width, height, item))
        img = img.astype(np.uint8)
        return img

    def ps_to_img(self, img1, delta_color):
        return ps_to_img(img1, delta_color)

    def _find_pic(self, img1, pic_name, delta_color, sim, method):
        img_path = self.path + os.path.sep + pic_name
        if not os.path.exists(img_path):
            raise f"图片路径不存在{img_path}"
        img2 = self.imread(img_path)
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        # img1 = self.ps_to_img(img1, delta_color)
        # img2 = self.ps_to_img(img2, delta_color)
        # if gray:
        #     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # 转灰度单通道
        #     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # 转灰度单通道
        #     ret, img1 = cv2.threshold(img1, 0, 254, 0)  # 二值化
        #     ret, img2 = cv2.threshold(img2, 0, 254, 0)  # 二值化
        # result = cv2.matchTemplate(img1, img2, method)
        if method <= 5:
            # 只匹配指定的颜色图像，参数mask表示参与匹配的像素矩阵
            if delta_color and isinstance(delta_color, str):
                lower, upper = color_to_range(delta_color, 1.0)
                lower, upper = lower_upper21(lower, upper)
                mask = cv2.inRange(img2, tuple(lower), tuple(upper))
            elif delta_color and (isinstance(delta_color, list) or isinstance(delta_color, tuple)):
                lower, upper = delta_color
                # lower, upper = lower_upper21(lower, upper)
                img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(img2_hsv, tuple(lower), tuple(upper))
            else:
                mask = None
            result = cv2.matchTemplate(img1, img2, method, mask=mask)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            yloc, xloc = np.where(result >= sim)
            height, width = img2.shape[:2]
            return result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width
        elif method == 6:
            return self._find_pic_BRISK(img1, img2, delta_color, sim)

    def _findPic(self, x1, y1, x2, y2, pic_name, delta_color, sim, method, capture=True):
        # 读取图片
        if capture:
            ret = self.capture(x1, y1, x2, y2)
            if ret:
                img1 = self.getCVImg()
            else:
                raise "截圖失敗"
        else:
            img1 = self.getCVImg()
        return self._find_pic(img1, pic_name, delta_color, sim, method)

    # 单点比色
    def cmpColor(self, x, y, color, sim=1):
        """
        :param x: 坐标x
        :param y: 坐标y
        :param color: 颜色字符串,可以支持偏色,"ffffff-202020",最多支持一个
        :param sim:相似度(0.1-1.0) (0,255)
        :return:bool
        """
        ret = self.capture(0, 0, 0, 0)
        if ret:
            img = self.getCVImg()
        else:
            raise "截圖失敗"
        lower, upper = color_to_range(color, sim)
        if not lower is None:
            new_color = img[y, x]
            for i in [0, 1, 2]:
                if new_color[i] < lower[i] or new_color[i] > upper[i]:
                    return False
            return True
        return False

    # 范围找色
    def findColor(self, x1, y1, x2, y2, color, sim):
        ret = self.capture(x1, y1, x2, y2)
        if ret:
            img = self.getCVImg()
        else:
            raise "截圖失敗"
        lower, upper = color_to_range(color, sim)
        img_array = np.array(img)
        mask1 = np.all(img_array >= lower, axis=-1)
        mask2 = np.all(img_array <= upper, axis=-1)
        mask = np.logical_and(mask1, mask2)
        pos = np.argwhere(mask)
        if len(pos):
            return pos[0]

    # BRISK 特征检测器
    def _find_pic_BRISK(self, img1, img2, delta_color, sim, drag=False):
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        img1 = self.ps_to_img(img1, delta_color)
        img2 = self.ps_to_img(img2, delta_color)
        # 初始化BRISK特征检测器
        brisk = cv2.BRISK_create()
        # 在a和b中检测关键点和描述符
        kp1, des1 = brisk.detectAndCompute(img1, None)
        kp2, des2 = brisk.detectAndCompute(img2, None)
        des1 = des1.astype('float32')
        des2 = des2.astype('float32')
        # 创建FLANN匹配器
        flann = cv2.FlannBasedMatcher()

        # 使用FLANN匹配器进行匹配
        matches = flann.knnMatch(des1, des2, k=2)

        # 定义比较函数
        def compare_ratio(match):
            # 返回第一个特征描述符距离与第二个特征描述符距离的比率
            return match[0].distance / match[1].distance

        # 进行排序
        matches = sorted(matches, key=compare_ratio)
        # 使用SANSAC过滤器进行匹配点过滤
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        if drag:
            imgshow(img_matches)
        if good_matches:
            return good_matches, kp1, img_matches

    def findTzPic(self, x1=0, y1=0, x2=None, y2=None, pic_name="", delta_color="", drag=None, capture=True):
        resoult = self._findPic(x1, y1, x2, y2, pic_name, delta_color, None, 6, capture)
        if resoult:
            good_matches, kp1, img = resoult
            m = good_matches[0]
            if drag:
                imgshow(img)
            # 浮点数转整数
            pts1 = np.array(kp1[m.queryIdx].pt, dtype=np.float32).astype(np.int32)
            return list(pts1)

    # 找图
    def findPic(self, x1=0, y1=0, x2=None, y2=None, pic_name="", delta_color="", sim=0.9, method=5, drag=None, capture=True, center=None):
        """
        :param center:
        :param x1:区域的左上X坐标
        :param y1:区域的左上Y坐标
        :param x2:区域的右下X坐标
        :param y2:区域的右下Y坐标
        :param pic_name:图片名，只能单个图片
        :param delta_color:偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
        :param sim:相似度，和算法相关
        :param method:仿大漠，总共有6总，范围0-5,对应cv的算法
        :param drag:是否在找到的位置画图并显示,默认不画
               方差匹配方法：匹配度越高，值越接近于0。
               归一化方差匹配方法：完全匹配结果为0。
               相关性匹配方法：完全匹配会得到很大值，不匹配会得到一个很小值或0。
               归一化的互相关匹配方法：完全匹配会得到1， 完全不匹配会得到0。
               相关系数匹配方法：完全匹配会得到一个很大值，完全不匹配会得到0，完全负相关会得到很大的负数。
                    （此处与书籍以及大部分分享的资料所认为不同，研究公式发现，只有归一化的相关系数才会有[-1,1]的值域）
               归一化的相关系数匹配方法：完全匹配会得到1，完全负相关匹配会得到-1，完全不匹配会得到0。
        :param capture:是否截图，或者使用之前的图片
        :param center:算法

        :return:
        """
        resoult = self._findPic(x1, y1, x2, y2, pic_name, delta_color, sim, method, capture)
        result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width = resoult
        # 画图
        if len(xloc):
            x, y = max_loc[0] + x1, max_loc[1] + y1
            if drag:
                img = cv2.rectangle(self.getCVImg(), (x, y), (x + width, y + height), (255, 0, 0), thickness=2)
                imgshow(img)
            if center:
                return x + width / 2, y + height / 2
            return x, y

    # 找图，返回多个匹配地址
    def findPics(self, x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None, capture=True):
        locs = []
        result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width = self._findPic(x1, y1, x2, y2, pic_name,
                                                                                              delta_color, sim,
                                                                                              method, capture)
        if len(xloc):
            if drag:
                for loc in zip(xloc, yloc):
                    img = cv2.rectangle(self.getCVImg(), (loc[0], loc[1]), (loc[0] + width, loc[1] + height),
                                        (255, 0, 0),
                                        thickness=2)
                    imgshow(img)
            locs = list(zip(xloc, yloc))
        return locs
        # return -1, [-1, -1]

    @staticmethod
    def imread(path):
        # 读取图片
        if PicColor.is_chinese(path):
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)  # 避免路径有中文
        else:
            img = cv2.imread(path)
        return img

    # 显示图像
    @staticmethod
    def imshow(img=None):
        """
        :param img:  cv格式图像
        :return: None
        """
        if img is None:
            raise "图像为空"
        cv2.imshow("img", img)
        cv2.waitKey(0)

    # 判断字符串是否为中文
    @staticmethod
    def is_chinese(string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def resize(self, fx=1, fy=1):
        """
        :param fx: x轴缩放倍数
        :param fy: y轴缩放倍数
        :return: img
        """
        return cv2.resize(self.getCVImg(), None, fx=fx, fy=fy)
