# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 14:57
@Auth ： 大雄
@File ：window.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes.wintypes
import ctypes


class Window():
    winKernel32 = ctypes.windll.kernel32
    winuser32 = ctypes.windll.LoadLibrary('user32.dll')
    wingdi32 = ctypes.windll.LoadLibrary('gdi32.dll')
    winntdll = ctypes.windll.LoadLibrary('ntdll.dll')
    winwinmm = ctypes.windll.LoadLibrary('winmm.dll')

    @staticmethod
    def clientToScreen(hwnd, x, y) -> tuple:
        point = ctypes.wintypes.POINT()
        point.x = x
        point.y = y
        is_ok: bool = Window.winuser32.ClientToScreen(hwnd, ctypes.byref(point))
        if not is_ok:
            raise Exception('call ClientToScreen failed')
        return (point.x, point.y)

    @staticmethod
    def enumProcess(name) -> str:
        '''需安装psutil'''
        try:
            import psutil
        except:
            raise Exception("called EnumProcess failed:psutil not install")
        ret = []
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            pname = ''
            if pinfo['name'] != None:
                pname = pinfo['name'].upper()
            if name.upper() in pname:
                ret.append((pinfo['pid'], pinfo['create_time']))
        if len(ret) == 0:
            raise Exception("called EnumProcess failed:process not found")
        ret = sorted(ret, key=lambda x: x[1])
        ret = [str(i[0]) for i in ret]
        return ','.join(ret)

    @staticmethod
    def findWindow(class_, title) -> int:
        return Window.findWindowEx(None, class_, title)

    @staticmethod
    def findWindowEx(parent, class_, title) -> int:
        retArr = []

        def mycallback(hwnd, extra) -> bool:
            if not Window.winuser32.IsWindowVisible(hwnd):
                return True
            if class_.upper() not in Window.getWindowClass(hwnd).upper():
                return True
            if title.upper() not in Window.getWindowTitle(hwnd).upper():
                return True
            retArr.append(hwnd)
            return False

        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        Window.winuser32.EnumChildWindows(parent, CMPFUNC(mycallback), 0)
        if len(retArr) == 0:
            raise Exception('call FindWindow failed:Not Found Window')
        return retArr[0]

    @staticmethod
    def findWindowByProcessId(process_id, class_, title) -> int:
        retArr = []

        def mycallback(hwnd, extra) -> bool:
            if not Window.winuser32.IsWindowVisible(hwnd):
                return True
            lProcessId = ctypes.wintypes.LONG()
            Window.winuser32.GetWindowThreadProcessId(hwnd, ctypes.byref(lProcessId))
            if process_id != lProcessId.value:
                return True
            if class_.upper() not in Window.getWindowClass(hwnd).upper():
                return True
            if title.upper() not in Window.getWindowTitle(hwnd).upper():
                return True
            retArr.append(hwnd)
            return False

        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        Window.winuser32.EnumChildWindows(None, CMPFUNC(mycallback), 0)
        if len(retArr) == 0:
            raise Exception('call FindWindowByProcessId failed:Not Found Window')
        return retArr[0]

    @staticmethod
    def findWindowByProcess(process_name, class_, title) -> int:
        '''需安装psutil'''
        try:
            import psutil
        except:
            raise Exception("called FindWindowByProcess failed:psutil not install")
        retArr = []

        def mycallback(hwnd, extra) -> bool:
            if not Window.winuser32.IsWindowVisible(hwnd):
                return True
            lProcessId = Window.getWindowProcessId(hwnd)
            lProcessName = None
            try:  # 有些进程是无法打开的
                lProcessName = psutil.Process(lProcessId).name()
            except:
                return True
            if (lProcessName == None): lProcessName = ""
            if process_name.upper() not in lProcessName.upper():
                return True
            if class_.upper() not in Window.getWindowClass(hwnd).upper():
                return True
            if title.upper() not in Window.getWindowTitle(hwnd).upper():
                return True
            retArr.append(hwnd)
            return False

        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        Window.winuser32.EnumChildWindows(None, CMPFUNC(mycallback), 0)
        if len(retArr) == 0:
            raise Exception('call FindWindowByProcessId failed:Not Found Window')
        return retArr[0]

    @staticmethod
    def getProcessInfo(pid):
        '''需安装psutil'''
        try:
            import psutil
        except:
            raise Exception("called GetProcessInfo failed:psutil not install")
        p = psutil.Process(pid)
        return p.name() + '|' + p.exe() + '|' + str(p.cpu_percent()) + '|' + str(p.memory_info().rss)

    @staticmethod
    def getWindowClass(hwnd) -> str:
        classStr = ctypes.create_string_buffer(''.encode(), 1000)
        is_ok: bool = Window.winuser32.GetClassNameA(hwnd, classStr, 1000)
        if (not is_ok) and Window.winKernel32.GetLastError() != 0:
            raise Exception("call GetWindowClass failed")
        return ctypes.string_at(classStr).decode('GB2312')

    @staticmethod
    def getWindowProcessId(hwnd) -> int:
        lProcessId = ctypes.wintypes.LONG()
        is_ok: bool = Window.winuser32.GetWindowThreadProcessId(hwnd, ctypes.byref(lProcessId))
        if (not is_ok) and Window.winKernel32.GetLastError() != 0:
            raise Exception("call GetWindowProcessId failed")
        return lProcessId.value

    @staticmethod
    def getWindowTitle(hwnd) -> str:
        titleStr = ctypes.create_string_buffer(''.encode(), 1000)
        is_ok: bool = Window.winuser32.GetWindowTextA(hwnd, titleStr, 1000)
        if (not is_ok) and Window.winKernel32.GetLastError() != 0:
            raise Exception("call GetWindowTitle failed")
        return ctypes.string_at(titleStr).decode('GB2312')

    @staticmethod
    def getWindowProcessPath(hwnd) -> str:
        '''需安装psutil'''
        try:
            import psutil
        except:
            raise Exception("called GetWindowProcessPath failed:psutil not install")
        process_id = Window.getWindowProcessId(hwnd)
        p = psutil.Process(process_id)
        return p.exe()

    @staticmethod
    def getSpecialWindow(flag) -> int:
        if flag == 0:
            return Window.winuser32.GetDesktopWindow()
        elif flag == 1:
            return Window.winuser32.FindWindowW("Shell_TrayWnd", 0)
        else:
            raise Exception('call GetSpecialWindow Failed')

    @staticmethod
    def getForegroundWindow() -> int:
        is_ok: int = Window.winuser32.GetForegroundWindow()
        if not is_ok:
            raise Exception('call GetForegroundWindow Failed')
        return is_ok

    @staticmethod
    def getForegroundFocus() -> int:
        wnd: int = Window.getForegroundWindow()
        if not wnd:
            raise Exception('call GetForegroundFocus Failed')
        SelfThreadId = Window.winKernel32.GetCurrentThreadId()
        ForeThreadId = Window.winuser32.GetWindowThreadProcessId(wnd, 0)
        Window.winuser32.AttachThreadInput(ForeThreadId, SelfThreadId, True)
        wnd = Window.winuser32.GetFocus()
        Window.winuser32.AttachThreadInput(ForeThreadId, SelfThreadId, False)
        if not wnd:
            raise Exception('call GetForegroundFocus Failed')
        return wnd

    @staticmethod
    def getMousePointWindow() -> int:
        class POINT(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.wintypes.LONG),
                ("y", ctypes.wintypes.LONG)
            ]

        point = POINT()
        Window.winuser32.GetCursorPos(ctypes.byref(point))
        hwnd = Window.winuser32.WindowFromPoint(point)
        if not hwnd:
            raise Exception('call GetMousePointWindow failed')
        return hwnd

    @staticmethod
    def getPointWindow(x, y) -> int:
        class POINT(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.wintypes.LONG),
                ("y", ctypes.wintypes.LONG)
            ]

        point = POINT()
        point.x = x
        point.y = y
        hwnd = Window.winuser32.WindowFromPoint(point)
        if not hwnd:
            raise Exception('call GetMousePointWindow failed')
        return hwnd

    @staticmethod
    def getWindow(hwnd, flag) -> int:
        rethwnd = None
        if flag == 0:
            rethwnd = Window.winuser32.GetParent(hwnd)
        elif flag == 1:
            rethwnd = Window.winuser32.GetWindow(hwnd, 5)
            # def mycallback(hwnd,extra) -> bool:
            #     nonlocal rethwnd
            #     rethwnd = hwnd
            #     return False
            # CMPFUNC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL,ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            # Window.winuser32.EnumChildWindows(hwnd,CMPFUNC(mycallback),0)
        elif flag == 2:
            rethwnd = Window.winuser32.GetWindow(hwnd, 0)
        elif flag == 3:
            rethwnd = Window.winuser32.GetWindow(hwnd, 1)
        elif flag == 4:
            rethwnd = Window.winuser32.GetWindow(hwnd, 2)
        elif flag == 5:
            rethwnd = Window.winuser32.GetWindow(hwnd, 3)
        elif flag == 6:
            rethwnd = Window.winuser32.GetWindow(hwnd, 4)
            if not rethwnd:
                rethwnd = Window.winuser32.GetParent(hwnd)
            if not rethwnd:
                rethwnd = hwnd
        elif flag == 7:
            rethwnd = Window.winuser32.GetTopWindow(hwnd)
            # top = hwnd
            # while True:
            #     hd = Window.winuser32.GetParent(top)
            #     if not hd:
            #         rethwnd = top
            #         break
            #     top = hd
        if not rethwnd:
            raise Exception('call GetWindow failed')
        return rethwnd

    @staticmethod
    def getWindowRect(hwnd) -> tuple:
        rect = ctypes.wintypes.RECT()
        is_ok: bool = Window.winuser32.GetWindowRect(hwnd, ctypes.byref(rect))
        if not is_ok:
            raise Exception('call GetWindowRect failed')
        return (rect.left, rect.top, rect.right, rect.bottom)

    @staticmethod
    def getWindowState(hwnd, flag) -> bool:
        if flag == 0:
            return Window.winuser32.IsWindow(hwnd) == 1
        elif flag == 1:
            return Window.getForegroundWindow() == hwnd
        elif flag == 2:
            return Window.winuser32.IsWindowVisible(hwnd) == 1
        elif flag == 3:
            return Window.winuser32.IsIconic(hwnd) == 1
        elif flag == 4:
            return Window.winuser32.IsZoomed(hwnd) == 1
        elif flag == 5:
            GWL_EXSTYLE = -20
            WS_EX_TOPMOST = 0x00000008
            if (Window.winuser32.GetWindowLongA(hwnd, GWL_EXSTYLE) & WS_EX_TOPMOST):
                return True
            else:
                return False
        elif flag == 6 or flag == 8:
            return Window.winuser32.IsHungAppWindow(hwnd) == 1
        elif flag == 7:
            return Window.winuser32.IsWindowEnabled(hwnd) == 1
        elif flag == 9:
            def Is64Bit() -> bool:
                class _SYSTEM_INFO(ctypes.Structure):
                    _fields_ = [
                        ("dwOemId", ctypes.wintypes.DWORD),
                        ("dwProcessorType", ctypes.wintypes.DWORD),
                        ("lpMinimumApplicationAddress", ctypes.wintypes.LPVOID),
                        ("lpMaximumApplicationAddress", ctypes.wintypes.LPVOID),
                        ("dwActiveProcessorMask", ctypes.wintypes.LPVOID),
                        ("dwNumberOfProcessors", ctypes.wintypes.DWORD),
                        ("dwProcessorType", ctypes.wintypes.DWORD),
                        ("dwAllocationGranularity", ctypes.wintypes.DWORD),
                        ("wProcessorLevel", ctypes.wintypes.WORD),
                        ("wProcessorRevision", ctypes.wintypes.WORD),
                    ]

                lpSystemInfo = _SYSTEM_INFO()
                Window.winKernel32.GetNativeSystemInfo(ctypes.byref(lpSystemInfo))
                PROCESSOR_ARCHITECTURE_IA64 = 6
                PROCESSOR_ARCHITECTURE_AMD64 = 9
                if lpSystemInfo.dwOemId in [PROCESSOR_ARCHITECTURE_IA64, PROCESSOR_ARCHITECTURE_AMD64]:
                    return True
                else:
                    return False

            if not Is64Bit():
                return False
            isWow64Process = ctypes.wintypes.BOOL(True)
            processId = Window.getWindowProcessId(hwnd)
            PROCESS_QUERY_INFORMATION = 0x0400
            hProcess = Window.winKernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, processId)
            if not hProcess:
                raise Exception('call GetWindowState failed:OpenProcess')
            is_ok: bool = Window.winKernel32.IsWow64Process(hProcess, ctypes.pointer(isWow64Process))
            Window.winKernel32.CloseHandle(hProcess)
            if not is_ok:
                raise Exception('call GetWindowState failed:IsWow64Process')
            if isWow64Process.value:
                return False
            return True

    @staticmethod
    def getClientSize(hwnd) -> tuple:
        rect = ctypes.wintypes.RECT()
        is_ok: bool = Window.winuser32.GetClientRect(hwnd, ctypes.byref(rect))
        if not is_ok:
            raise Exception('call GetClientRect failed')
        return (rect.right, rect.bottom)

    @staticmethod
    def screenToClient(hwnd, x, y) -> tuple:
        point = ctypes.wintypes.POINT()
        point.x = x
        point.y = y
        is_ok: bool = Window.winuser32.ScreenToClient(hwnd, ctypes.byref(point))
        if not is_ok:
            raise Exception('call ScreenToClient failed')
        return (point.x, point.y)

    @staticmethod
    def getClientRect(hwnd) -> tuple:
        x1, y1 = Window.clientToScreen(hwnd, 0, 0)
        x2, y2 = Window.getClientSize(hwnd)
        x2, y2 = Window.clientToScreen(hwnd, x2, y2)
        return (x1, y1, x2, y2)

    @staticmethod
    def moveWindow(hwnd, x, y) -> None:
        x1, y1, x2, y2 = Window.getWindowRect(hwnd)
        is_ok: bool = Window.winuser32.MoveWindow(hwnd, 0, 0, x2 - x1, y2 - y1, True)
        if not is_ok:
            raise Exception('call MoveWindow failed')

    @staticmethod
    def setWindowSize(hwnd, width, height) -> None:
        x1, y1, x2, y2 = Window.getWindowRect(hwnd)
        is_ok: bool = Window.winuser32.MoveWindow(hwnd, x1, y1, width, height, True)
        if not is_ok:
            raise Exception('call SetWindowSize failed')

    @staticmethod
    def setWindowText(hwnd, title):
        is_ok: bool = Window.winuser32.SetWindowTextW(hwnd, title)
        if not is_ok:
            raise Exception('call SetWindowText failed')

    @staticmethod
    def setWindowTransparent(hwnd, trans):
        is_ok: bool = Window.winuser32.SetLayeredWindowAttributes(hwnd, 0, trans, 2)
        if not is_ok:
            raise Exception('call SetWindowTransparent failed')

    @staticmethod
    def setClientSize(hwnd, width, height) -> None:
        wx1, wy1, wx2, wy2 = Window.getWindowRect(hwnd)
        w, h = Window.getClientSize(hwnd)
        Window.setWindowSize(hwnd, wx2 - wx1 + width - w, wy2 - wy1 + height - h)

    @staticmethod
    def sendPaste(hwnd) -> None:
        class WINDOWPLACEMENT(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.wintypes.UINT),
                ("flags", ctypes.wintypes.UINT),
                ("showCmd", ctypes.wintypes.UINT),
                ("ptMinPosition", ctypes.wintypes.POINT),
                ("ptMaxPosition", ctypes.wintypes.POINT),
                ("rcNormalPosition", ctypes.wintypes.RECT)
            ]

        if not Window.getWindowState(hwnd, 0):
            raise Exception('call SendPaste failed:window not exist')
        wtp = WINDOWPLACEMENT()
        Window.winuser32.GetWindowPlacement(hwnd, ctypes.byref(wtp))
        if (wtp.showCmd != 1):  # 没有最小化
            if wtp.showCmd == 2:  # 被最小化了
                wtp.showCmd = 9
                Window.winuser32.SetWindowPlacement(hwnd, ctypes.byref(wtp))
        # 正常情况下wtp.showCmd为3，表示前台
        Window.winuser32.SetForegroundWindow(hwnd)
        Window.winuser32.BringWindowToTop(hwnd)
        Window.winuser32.keybd_event(0x11, 0, 0x0001, 0);
        Window.winuser32.keybd_event(86, 0, 0x0001, 0);
        Window.winuser32.keybd_event(86, 0, 0x0001 | 0x0002, 0)
        Window.winuser32.keybd_event(0x11, 0, 0x0001 | 0x0002, 0)

    @staticmethod
    def setWindowState(hwnd, flag):
        class WINDOWPLACEMENT(ctypes.Structure):
            _fields_ = [
                ("length", ctypes.wintypes.UINT),
                ("flags", ctypes.wintypes.UINT),
                ("showCmd", ctypes.wintypes.UINT),
                ("ptMinPosition", ctypes.wintypes.POINT),
                ("ptMaxPosition", ctypes.wintypes.POINT),
                ("rcNormalPosition", ctypes.wintypes.RECT)
            ]

        is_ok = False
        if flag == 0:
            is_ok = Window.winuser32.SendMessageW(hwnd, 0x0010, 0, 0)
        elif flag == 1:
            is_ok = Window.winuser32.SetActiveWindow(hwnd)
        elif flag == 2 or flag == 3:
            is_ok = Window.winuser32.ShowWindow(hwnd, 2)
        elif flag == 4:
            is_ok = Window.winuser32.ShowWindow(hwnd, 3)
            is_ok = Window.winuser32.SetActiveWindow(hwnd)
        elif flag == 5:
            wtp = WINDOWPLACEMENT()
            is_ok = Window.winuser32.GetWindowPlacement(hwnd, ctypes.byref(wtp))
            wtp.showCmd = 9
            is_ok = Window.winuser32.SetWindowPlacement(hwnd, ctypes.byref(wtp))
        elif flag == 6:
            wtp = WINDOWPLACEMENT()
            is_ok = Window.winuser32.GetWindowPlacement(hwnd, ctypes.byref(wtp))
            wtp.showCmd = 0
            is_ok = Window.winuser32.SetWindowPlacement(hwnd, ctypes.byref(wtp))
        elif flag == 7:
            wtp = WINDOWPLACEMENT()
            is_ok = Window.winuser32.GetWindowPlacement(hwnd, ctypes.byref(wtp))
            wtp.showCmd = 5
            is_ok = Window.winuser32.SetWindowPlacement(hwnd, ctypes.byref(wtp))
        elif flag == 8:
            is_ok = Window.winuser32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 3)
        elif flag == 9:
            is_ok = Window.winuser32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 3)
        elif flag in [10, 11, 12]:
            pass
        elif flag == 13:
            pid = Window.getWindowProcessId(hwnd)
            hProcessHandle = Window.winKernel32.OpenProcess(1, False, pid)
            is_ok = Window.winKernel32.TerminateProcess(hProcessHandle, 4)
            Window.winKernel32.CloseHandle(hProcessHandle)
        elif flag == 14:
            is_ok = Window.winuser32.FlashWindow(hwnd, True)
        elif flag == 15:
            hCurWnd = Window.winuser32.GetForegroundWindow()
            dwMyID = Window.winKernel32.GetCurrentThreadId()
            dwCurID = Window.winuser32.GetWindowThreadProcessId(hCurWnd, 0)
            Window.winuser32.AttachThreadInput(dwCurID, dwMyID, True)
            is_ok = Window.winuser32.SetFocus(hwnd)
            Window.winuser32.AttachThreadInput(dwCurID, dwMyID, False)
        if not is_ok:
            raise Exception('窗口设置失败,请检查句柄或者参数')

    @staticmethod
    def enumWindow(parent_, title, class_name, filter):
        if not parent_:
            parent_ = Window.getSpecialWindow(0)
        martchVec = []

        def mycallback(hwnd, extra) -> bool:
            wtitle = None
            wclass = None
            try:
                wtitle = Window.getWindowTitle(hwnd)
                wclass = Window.getWindowClass(hwnd)
            except:
                return True
            if filter & 1 == 1:
                if title.upper() not in wtitle.upper():
                    return True
            if ((filter & 2) >> 1) == 1:
                if class_name.upper() not in wclass.upper():
                    return True
            if ((filter & 4) >> 2) == 1:
                try:
                    if Window.getWindow(hwnd, 0) != parent_:
                        return True
                except:
                    return True
            if ((filter & 8) >> 3) == 1:
                if not (Window.winuser32.GetParent(hwnd) == 0):
                    return True
                if Window.winKernel32.GetLastError() != 0:
                    return True
            if ((filter & 16) >> 4) == 1:
                if Window.getWindowState(2, ) == False:
                    return True
            martchVec.append(hwnd)
            return True

        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        Window.winuser32.EnumChildWindows(parent_, CMPFUNC(mycallback), 0)
        if len(martchVec) == 0:
            raise Exception('call EnumWindow failed:not found any window')
        return ','.join([str(i) for i in martchVec])
