# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/5 1:35
@Auth ： 大雄
@File ：ocr_normal.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os
import threading
from io import BytesIO
from PyDmGame.modular.publicFunction import *
from PyDmGame.modular.ocr_.PPOCR_api import PPOCR
from PyDmGame.model.model import dmgl_info, dmtd_info


class Ocr_normal:
    def __init__(self):
        project_path = os.path.join(os.path.dirname(__file__), )
        path = project_path + os.path.sep + "PaddleOCR-json.v1.2.1\\PaddleOCR_json.exe"
        if not dmgl_info.ppocr is None:
            self._ppocr = dmgl_info.ppocr
        else:
            self._ppocr = PPOCR(path)
            dmgl_info.ppocr = self._ppocr
        self.temp_path = project_path + os.path.sep + f"temp\\{self.id}.bmp"
        self.Lock = threading.Lock()
        self.save_flag = True

    def set_ocr_save(self, save_flag):
        self.save_flag = save_flag

    # 查找数字是否存在
    def findNum(self, x1, y1, x2, y2, numString, color_format, sim):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param numString: 字符串:如数字"1","56","789"
        :param color_format:字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
        :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
        :return:bool
        """
        if numString in str(self.ocrNum(x1, y1, x2, y2, color_format, sim, )):
            return True
        return False

    # 识别数字
    def ocrNum(self, x1, y1, x2, y2, color_format, sim, dirPath):
        """
        :param x1:  x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param color_format: 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
        :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
        :param dirPath: 图库路径,用于存储0-9数字模板
        :return: num：字符串数字
        """
        num_dict = {}
        # 遍历图像,并挨个识别
        for i in range(10):
            img_num = dirPath + os.path.sep + f"{i}.bmp"
            ret, locs = self.FindPics(x1, y1, x2, y2, img_num, color_format, sim)
            if ret != -1:
                for loc in locs:
                    num_dict.update({loc[0]: i})
        # 排序字典
        new_num_list = sorted(num_dict.items(), key=lambda x: x[0])  # 对x轴进行排序

        # 遍历并拼接数字
        nums = "".join([str(new_num[1]) for new_num in new_num_list])
        try:
            return nums
        except:
            return ""

    def _saveImg(self, img):
        if self.save_flag:
            cv2.imwrite(self.temp_path, img)
            return self.temp_path
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            is_success, buffer = cv2.imencode(".BMP", img)
            output = BytesIO(buffer)
            data = output.getvalue()[14:]
            output.close()
            send_msg_to_clip(win32clipboard.CF_DIB, data)
            return "clipboard"

    def _ocr_son(self,img,color_format,sim):
        img = ps_to_img(img, color_format)
        with self.Lock:
            stdint = self._saveImg(img)
            result = self._ppocr.run(stdint)
        if result["code"] == 100:
            new_result = []
            for dic in result["data"]:
                if dic["score"] >= sim:
                    new_result.append(dic)
            return new_result

    def _ocr(self, x1, y1, x2, y2, color_format, sim):
        self.capture(x1, y1, x2, y2)
        img = self._img
        result = self._ocr_son(img,color_format,sim)
        return result

    # 识别文字
    def ocr(self, x1, y1, x2, y2, color_format, sim):
        result = self._ocr(x1, y1, x2, y2, color_format, sim)
        return result

    # 查找文字
    def FindStr(self, x1, y1, x2, y2, string, color_format, sim):
        result = self._ocr(x1, y1, x2, y2, color_format, sim)
        if result["code"] == 100:
            for dic in result["data"]:
                if dic["score"] >= sim and string in dic["text"]:
                    return dic["box"][0]
