# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/12 11:23
@Auth ： 大雄
@File ：ocr.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os



class Ocr:
    # # 设置服务器地址
    # def SetServerUrl(self,url):
    #     self.ocr_server_url = url

    # 查找数字是否存在
    def FindNum(self, x1, y1, x2, y2, numString, color_format, sim):
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
        if numString in str(self.OcrNum(x1, y1, x2, y2, color_format, sim)):
            return True
        return False

    # 识别数字
    def OcrNum(self, x1, y1, x2, y2, color_format, sim, dirPath):
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

    # # 服务器ocr
    # def OcrServer(self, x1, y1, x2, y2, color_format, sim):
    #     """
    #     :param x1: 整形数:区域的左上X坐标
    #     :param y1: 整形数:区域的左上Y坐标
    #     :param x2: 整形数:区域的右下X坐标
    #     :param y2: 整形数:区域的右下Y坐标
    #     :param color_format: 偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
    #     :param sim: 相似度
    #     :return: 列表,包含坐标和文字
    #     """
    #     if not None in [x1, y1, x2, y2]:
    #         img = self.img[y1:y2, x1:x2]
    #     img = self.__ps_to_img(img, color_format)
    #     img_bt = np.array(cv2.imencode('.png', img)[1]).tobytes()
    #     data = {
    #         'username': 270207756,
    #         'pwd': 123456,
    #         'lang': "ch",  # ch中文,eh英文
    #         "det": True,  # 是指是否要检测文本的位置,False为识别单行，Ture为识别多行，只有多行才有坐标返回
    #         "ret": True,  # 是指是否要识别文本的内容
    #         "file":io.BytesIO(img_bt)
    #     }
    #     data = urllib.parse.urlencode(data).encode('utf8')
    #     request = urllib.request.Request(self.ocr_server_url, data=data,method="post")
    #     response  = urllib.request.urlopen(request)
    #     # response = requests.post(self.ocr_server_url, files=[('img', ("", file))], data=data)
    #     if response.status_code == 200:
    #         result = response.json()
    #         msg_code = result["msg_code"]
    #         if msg_code == 200:
    #             content = result["content"]
    #             result = [item for item in content[0] if item[1][1] > sim]
    #             new_result = []
    #             for item in result:
    #                 item[0] = [[loc[0] + x1, loc[1] + y1] for loc in item[0]]
    #                 new_result.append(item)
    #             return new_result
    #         else:
    #             print(f"识别异常 {response.json()}")
    #
    #     else:
    #         print(f"服务器异常 {response.status_code}")
    #         return False