# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/6 15:54
@Auth ： 大雄
@File ：ld.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import json
import os
import random
import time
from xml.dom.minidom import parseString


class Dnconsole:
    # 设置雷电路径
    def set_ld_path(self, console_path):
        # 请根据自己电脑配置
        console_path = os.path.dirname(console_path)
        self._console = console_path + "\\ldconsole.exe "  # 和dnonsole的区别是一个显示，一个隐藏
        self._ld = console_path + "\\ld.exe "
        self._setting_path = console_path + "\\vms\\config"
        self._max_list = None  # 存储所有模拟器列表信息



    # 设置雷电序号
    def set_ldNum(self, ldNum):
        self._index = ldNum
        self.ld_temp_image = self.get_config('statusSettings.sharedPictures')
        # self.set_sharedPictures(self.ld_temp_image)

    def get_ldNum(self):
        return self._index

    # 获取模拟器列表
    def get_list(self, out_ldNums=None, check_=True):
        """
        :param out_ldNums: 排除的模拟器
        :param check:检查第一次和第下次的模拟器数量是否一致
        :return:每个模拟器列表包含：索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        """

        def get_info():
            cmd = os.popen(self._console + 'list2')
            text = cmd.read()
            cmd.close()
            return text.split('\n')

        result = list()
        info = get_info()
        # 是否开启检查数量,避免雷电获取的命令信息有缺
        if check_ and self._max_list:
            for i in range(10):
                if len(info) == self._max_list:
                    break
                else:
                    time.sleep(1)
                    info = get_info()
            else:
                raise "模拟器获取数量不一致"
        else:
            self._max_list = len(info)

        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                # 去除模拟器序号
                if out_ldNums and type(out_ldNums) == list:
                    if int(dnplayer[0]) in out_ldNums:
                        continue
                result.append(DnPlayer(dnplayer))
        return result

    # 获取正在运行的模拟器列表
    def list_running(self) -> list:
        result = list()
        all__ = self.get_list()
        for dn in all__:
            if dn.is_running() is True:
                result.append(dn)
        return result

    # 检测指定序号的模拟器是否正在运行
    def is_running(self) -> bool:
        all__ = self.get_list()
        for item in all__:
            if int(item.index) == self._index:
                return item.is_in_android

    # 执行shell命令
    def dnld(self, command: str, silence: bool = True):
        cmd = self._ld + '-s %d %s' % (self._index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 执行adb命令,不建议使用,容易失控
    def adb(self, command: str, silence: bool = False) -> str:
        cmd = self._console + 'adb --index %d --command "%s"' % (self._index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 安装apk 指定模拟器必须已经启动
    def install(self, path__: str):
        cmd = self._console + 'installapp --index %d --filename %s' % (self._index, path__)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 卸载apk 指定模拟器必须已经启动
    def uninstall(self, package: str):
        cmd = self._console + 'uninstallapp --index %d --packagename %s' % (self._index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 启动App  指定模拟器必须已经启动
    def invokeapp(self, package: str):
        cmd = self._console + 'runapp --index %d --packagename %s' % (self._index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 停止App  指定模拟器必须已经启动
    def stopapp(self, package: str):
        cmd = self._console + 'killapp --index %d --packagename %s' % (self._index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取安装包列表
    def get_package_list(self) -> list:
        result = list()
        text = self.dnld('pm list packages', False)
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    # 检测是否安装指定的应用
    def has_install(self, package: str):
        if self.is_running() is False:
            return False
        return package in self.get_package_list()

    # 启动模拟器
    def launch(self):
        cmd = self._console + 'launch --index ' + str(self._index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 关闭模拟器
    def quit(self):
        cmd = self._console + 'quit --index ' + str(self._index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 重启模拟器，并打开指定应用
    def restart(self, packName):
        cmd = self._console + 'action --index %d --key call.reboot --value %s' % (self._index, packName)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920 下次启动时生效
    def set_screen_size(self, width, hight, dip):
        cmd = self._console + f'modify --index %d --resolution {width},{hight},{dip}' % self._index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 复制模拟器,被复制的模拟器不能启动
    def copy_simulator(self, name: str):
        cmd = self._console + 'copy --name %s --from %d' % (name, self._index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 添加模拟器
    def add_simulator(self, name: str):
        cmd = self._console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置自动旋转
    def auto_rate(self, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = self._console + 'modify --_index %d --autorotate %d' % (self._index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变设备信息 imei imsi simserial androidid mac值
    def change_device_data(self):
        # 改变设备信息
        cmd = self._console + 'modify --_index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % self._index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变CPU数量
    def change_cpu_count(self, number: int):
        # 修改cpu数量
        cmd = self._console + 'modify --_index %d --cpu %d' % (self._index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def get_cur_activity_xml(self):
        # 获取当前activity的xml信息
        self.dnld('uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(self.ld_temp_image + '/activity.xml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    def get_user_info(self):
        xml = self.get_cur_activity_xml()
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    # 获取当前activity名称
    def get_activity_name(self):
        text = self.dnld('"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    # 等待某个activity出现
    def wait_activity(self, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if self.get_activity_name() == activity:
                return True
            time.sleep(1)
        return False

    # 自动排序
    def sort(self):
        cmd = self._console + "sortWnd"
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取图片保存路径
    def get_config(self,key_name=None):
        index_setting_path = self._setting_path + "\\leidian%s.config" % self._index
        with open(index_setting_path, "r+", encoding="utf-8") as fp:
            text = fp.read()
            if key_name is None:
                return text
            elif key_name in text:
                text = json.loads(text)
                return text[key_name]
    # 修改默认图片保存路径
    # def set_sharedPictures(self, path):
    #     set_name = 'statusSettings.sharedPictures'
    #     new_config = ""  # 写入的文件
    #     path = path.replace('\\', "/")
    #     index_setting_path = self._setting_path + "\\leidian%s.config" % self._index
    #     with open(index_setting_path, "r+", encoding="utf-8") as fp:
    #         text = fp.read()
    #         if set_name in text:
    #             # 路径已存在，不重复写入
    #             if path in text:
    #                 return
    #             # 参数存在,但是路径不对,替换路径
    #             else:
    #                 fp.seek(0)
    #                 all_line = fp.readlines()
    #                 for line in all_line:
    #                     if set_name in line:
    #                         line = f'\t"{set_name}": "{path}",\n'
    #                     new_config += line
    #         # 参数不存在时,使用雷电3模板替换文件，并随机在写入部分参数，分辨率默认为960*540*160*240
    #         else:
    #             with open(path + "\\leidian_template.config", "r", encoding="utf-8") as fp:
    #                 new_config = fp.read()
    #                 new_config = new_config.replace("save_image_path", path)
    #                 new_config = new_config.replace("phoneIMEI_num", str(Dnconsole.myRandom("int", 12)))
    #                 new_config = new_config.replace("phoneIMSI_num", str(Dnconsole.myRandom("int", 12)))
    #                 new_config = new_config.replace("phoneSimSerial_num", str(Dnconsole.myRandom("int", 20)))
    #                 new_config = new_config.replace("phoneAndroidId_num",
    #                                                 format(int(Dnconsole.myRandom("hex", 16)), 'x'))
    #                 new_config = new_config.replace("macAddress_num", format(int(Dnconsole.myRandom("hex", 12)), 'x'))
    #
    #         # 有更改时,重新写入数据
    #         with open(index_setting_path, "w", encoding="utf-8") as fp:
    #             fp.write(new_config)

    # 随机指定类型和长度的整数数字
    @staticmethod
    def myRandom(str_type, len_):
        if str_type == "int":
            multiplier = 10
        elif str_type == "hex":
            multiplier = 16
        min_num = pow(multiplier, len_ - 1)
        max_num = min_num * multiplier - 1
        num = random.randint(min_num, max_num)
        return num


class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])

        try:
            self.name = info[1]
            self.top_win_handler = int(info[2])
            self.bind_win_handler = int(info[3])
            self.is_in_android = True if int(info[4]) == 1 else False
            self.pid = int(info[5])
            self.vbox_pid = int(info[6])
        except:
            self.name = 0
            self.top_win_handler = 0
            self.bind_win_handler = 0
            self.is_in_android = False
            self.pid = 0
            self.vbox_pid = 0

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\n_index:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\n_index:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)


class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
            # 用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)
