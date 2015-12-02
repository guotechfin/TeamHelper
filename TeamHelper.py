# coding=gbk

import win32con
import win32gui
import win32api
import win32clipboard
import os
import time

user_list = {}
user_list['ly'] = {'name': 'ly', 'email': 'luoyang@pku.edu.cn', 'spell': 'luoyang'}

def QQ_setClipboardText(str):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, str)
    win32clipboard.CloseClipboard()

def QQ_PrintText(str):
    QQ_setClipboardText(str)
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, 0, 0);
    win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

def QQ_AtPerson(name):
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0);
    win32api.keybd_event(ord('2'), 0, 0, 0);
    win32api.keybd_event(ord('2'), 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0);

    time.sleep(0.2)

    QQ_setClipboardText(user_list[name]['spell'])

    time.sleep(0.2)

    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0);

def QQ_Enter():
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0);
    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0);
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0);

def QQ_SendTextWithAt(str):
    os.system('"C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe" /uin:515964173 /quicklunch:F78FE332AE3FCB7AF343769DCD59D8091DA84C9049606DF1795A0B398612FB587F6DBBFC30843359')

    try_time = 0
    while True:
        time.sleep(0.5)
        hwnd = win32gui.FindWindow(None, 'OSVT小O测试群')
        print ('try_time = %d, hwnd = %d' %(try_time, hwnd))
        if hwnd != 0:
            break
        elif try_time >= 60:
            print ('SendTextToQQ Error.')
            return
        else:
            try_time = try_time + 1

    win32gui.SetForegroundWindow(hwnd)

    QQ_PrintText(str)
    QQ_AtPerson('ly')
    QQ_PrintText(str)
    QQ_Enter()

    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('v'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord('v'), 0)


    #win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, 'aaa')
    #win32gui.SetWindowText(hwnd, 'aaa')
    #win32gui.ReplaceSel()
    #win32gui.PostMessage(hwnd, win32con.WM_CHAR, '他', 3)

    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord('V'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord('V'), 0)
    # win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)

QQ_SendTextWithAt('@OSVT助理小O 大家好！')
