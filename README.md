# PyDmGame

## 目录

## [安装](#1)

## [初始化](#2)

## [基本设置](#3)

## [后台设置](#4)

## [窗口](#5)

## [图色](#6)

## [键鼠](#7)

## [文字识别](#8)

## [虚拟按键码](#9)

### <a id="1"></a>安装

    pip install PyDmGame

### <a id="2"></a>初始化

    improt PyDmGame
    dm = PyDmGame.DM()
    dm.set_find_image_path("imagePath") # 设置默认找图路径,不使用找图可以不设置
    dm.BindWindow(hwnd,"normal","normal","windows",0) # 绑定模式,请参考后台设置

### <a id="3"></a>基本设置

#### SetPath(path)

    设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片
    :param path 字符串: 路径,绝对路径
    返回值:None

### <a id="4"></a>后台设置

#### BindWindow(hwnd,display,mouse,keypad,mode=0)

    绑定指定的窗口,并指定这个窗口的屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式,以及模式设定
    :param hwnd 整形数: 指定的窗口句柄
        display 字符串: 屏幕颜色获取方式 取值有以下几种
        "normal" : 正常模式,平常我们用的前台截屏模式
        "gdi" : gdi模式,用于窗口采用GDI方式刷新时
    
    :param mouse 字符串: 鼠标仿真模式 取值有以下几种
        "normal" : 正常模式,平常我们用的前台鼠标模式,api为SendInput函数
        "normal2" : 正常模式,平常我们用的前台鼠标模式,api为event事件,微软官方已废弃，被SendInput取代
        "windows": 后台模式,采取模拟windows消息方式 同按键自带后台插件,api为SendMessage函数,雷电模拟器可用这个模式
        "windows2": 后台模式,采取模拟windows消息方式 同按键自带后台插件,api为PostMessage函数
    
    :param keypad 字符串: 键盘仿真模式 取值有以下几种
        "normal" : 正常模式,平常我们用的前台鼠标模式,api为SendInput函数
        "normal2" : 正常模式,平常我们用的前台鼠标模式,api为event事件,微软官方已废弃，被SendInput取代
        "windows": 后台模式,采取模拟windows消息方式 同按键自带后台插件,api为SendMessage函数,雷电模拟器可用这个模式
        "windows2": 后台模式,采取模拟windows消息方式 同按键自带后台插件,api为PostMessage函数

    :param mode 整形数: 模式
        预留接口,此参数可不写
    返回值:None

### <a id="5"></a>窗口(未测试验证)

#### ClientToScreen(hwnd,x,y)

    把窗口坐标转换为屏幕坐标
    :param hwnd 整形数: 指定的窗口句柄
    :param x 变参指针: 窗口X坐标
    :param y 变参指针: 窗口Y坐标

#### EnumProcess(name)

    :param name 字符串:进程名,比如qq.exe
    返回值:返回所有匹配的进程PID,并按打开顺序排序,格式"pid1,pid2,pid3"

#### EnumWindow(parent,title,class_name,filter)

#### FindWindow(class,title)

#### FindWindowByProcess(process_name,class,title)

#### FindWindowByProcessId(process_id,class,title)

#### FindWindowEx(parent,class,title)

#### GetClientRect(hwnd,x1,y1,x2,y2)

#### GetClientSize(hwnd,width,height)

#### GetForegroundFocus()

#### GetForegroundWindow()

#### GetMousePointWindow()

#### GetPointWindow(x,y)

#### GetProcessInfo(pid)

#### GetSpecialWindow(flag)

#### GetWindow(hwnd,flag)

#### GetWindowClass(hwnd)

#### GetWindowProcessId(hwnd)

#### GetWindowProcessPath(hwnd)

#### GetWindowRect(hwnd,x1,y1,x2,y2)

#### GetWindowState(hwnd,flag)

#### GetWindowTitle(hwnd)

#### MoveWindow(hwnd,x,y)

#### ScreenToClient(hwnd,x,y)

#### SendPaste(hwnd)

#### SetClientSize(hwnd,width,height)

#### SetWindowSize(hwnd,width,height)

#### SetWindowState(hwnd,flag)

#### SetWindowText(hwnd,title)

#### SetWindowTransparent(hwnd,trans)

### <a id="6"></a>图色

#### Capture(x1, y1, x2, y2, file)

    抓取指定区域(x1, y1, x2, y2)的图像保存为file,图像后缀任意填写
    :param x1 整形数:区域的左上X坐标
    :param y1 整形数:区域的左上Y坐标
    :param x2 整形数:区域的右下X坐标
    :param y2 整形数:区域的右下Y坐标
    :param file 字符串:保存的文件名,填写绝对路径,不填写也可以，通过GetCVImg()获取CV图像

#### CmpColor(x, y, color, sim=1)

    比较指定坐标点(x,y)的颜色
    x 整形数: X坐标
    y 整形数: Y坐标
    color 字符串: 颜色字符串,可以支持偏色,支持RGB偏色和HSV偏色
    sim 双精度浮点数: 相似度(0.1-1.0)
    返回值:
        True颜色匹配
        False颜色不匹配

#### FindColor(x1, y1, x2, y2, color, sim, dir=None)

    查找指定区域内的颜色,支持RGB和HSV颜色
    :param x1 整形数:区域的左上X坐标
    :param y1 整形数:区域的左上Y坐标
    :param x2 整形数:区域的右下X坐标
    :param y2 整形数:区域的右下Y坐标
    :param color 字符串:颜色 格式为"RRGGBB-DRDGDB",比如"123456-000000",或者HSV格式((0,0,0),(180,255,255))
    :param sim 双精度浮点数:相似度,取值范围0.1-1.0
    :param dir 整形数:预留参数，可不写
    返回值:
        找到：0,x,y
        未找到:-1, -1, -1

#### FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None)

    查找指定区域内的图片,返回相似度最大的坐标,原来是利用opencv的模板匹配,默认使用算法5
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
    返回值:
        找到：0,x,y
        未找到:-1, -1, -1

#### FindPics(x1, y1, x2, y2, pic_name, delta_color, sim, method=5, drag=None)

    查找指定区域内的图片,返回多个坐标,原来是利用opencv的模板匹配,默认使用算法5
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
    返回值:
        找到：0,[[x1,y1],[x2,y2],...)]
        未找到:-1, -1, -1

#### GetCVImg()

    获取截图的内存图像,格式cv,需要先使用Capture截图

### <a id="7"></a>键鼠

#### GetCursorPos(x,y)

    获取鼠标位置
    :param x:鼠标横坐标
    :param y:鼠标束坐标

#### GetCursorShape()

    获取鼠标特征码
    成功时，返回鼠标特征码.  
    失败时，返回空的串.

#### LeftDown()

    按住鼠标左键

#### LeftUp()

    弹起鼠标左键

#### LeftClick()

    单击鼠标左键

#### LeftDoubleClick()

    双击鼠标左键

#### RightDown()

    按住鼠标右键

#### RightUp()

    弹起鼠标右键

#### RightClick()

    单击鼠标右键

#### SetMouseDelay(self,type,delay)

    设置鼠标单击或者双击时,鼠标按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常点击。
    :param type 字符串: 鼠标类型,取值有以下
        "normal" : 对应normal鼠标 默认内部延时为 30ms
        "windows": 对应windows 鼠标 默认内部延时为 10ms
    :paramd elay 整形数: 延时,单位是毫秒

#### MoveTo(x,y)

    把鼠标移动到目的点(x,y)
    :param x 整形数:X坐标
    :param y 整形数:Y坐标

#### WheelDown()

    滚轮向下滚

#### WheelUp()

    滚轮向上滚

#### SetKeypadDelay(delay=None)

    设置按键时,键盘按下和弹起的时间间隔。高级用户使用。某些窗口可能需要调整这个参数才可以正常按键。
    type 字符串: 键盘类型,取值有以下
        "normal" : 对应normal键盘  默认内部延时为30ms
        "windows": 对应windows 键盘 默认内部延时为10ms
    delay 整形数: 延时,单位是毫秒

#### KeyDownChar(key_str)

    按住指定的虚拟键码

#### KeyUpChar(key_str)

    弹起来虚拟键key_str

#### KeyPressChar(key_str)

    按下指定的虚拟键码

#### KeyPressStr(key_str,delay)

    根据指定的字符串序列，依次按顺序按下其中的字符.
    key_str 字符串: 需要按下的字符串序列. 比如"1234","abcd","7389,1462"等.
    delay 整形数: 每按下一个按键，需要延时多久. 单位毫秒.这个值越大，按的速度越慢。

#### SendString(hwnd,str)

    向指定窗口发送文本数据
    hwnd 整形数: 指定的窗口句柄. 如果为0,则对当前激活的窗口发送.
    str 字符串: 发送的文本数据

### <a id="8"></a>文字识别

#### FindNum(x1, y1, x2, y2, numString, color_format, sim)

    :param x1: x1 整形数:区域的左上X坐标
    :param y1: y1 整形数:区域的左上Y坐标
    :param x2: x2 整形数:区域的右下X坐标
    :param y2: y2 整形数:区域的右下Y坐标
    :param numString: 字符串:如数字"1","56","789"
    :param color_format:字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
    :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
    :return:bool

#### OcrNum(x1, y1, x2, y2, color_format, sim, dirPath)

    :param x1:  x1 整形数:区域的左上X坐标
    :param y1: y1 整形数:区域的左上Y坐标
    :param x2: x2 整形数:区域的右下X坐标
    :param y2: y2 整形数:区域的右下Y坐标
    :param color_format: 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
    :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
    :param dirPath: 图库路径,用于存储0-9数字模板
    :return: num：字符串数字

### <a id="9"></a>虚拟按键码
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
    'f13': 0x7C,
    'f14': 0x7D,
    'f15': 0x7E,
    'f16': 0x7F,
    'f17': 0x80,
    'f18': 0x81,
    'f19': 0x82,
    'f20': 0x83,
    'f21': 0x84,
    'f22': 0x85,
    'f23': 0x86,
    'f24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE}