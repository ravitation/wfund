#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import time
import hashlib
import random
import platform


def MakeBitmap(color):
    bmp = wx.Bitmap(16, 15)
    dc = wx.MemoryDC()
    dc.SelectObject(bmp)
    dc.SetBackground(wx.Brush(color))
    dc.Clear()
    dc.SelectObject(wx.NullBitmap)
    return bmp


def show_msg(msg=''):
    dlg = wx.MessageDialog(None, msg, 'A Message Box', wx.YES_NO)
    code = dlg.ShowModal()
    if code == wx.YES:
        dlg.Destroy()
    return code


def now_time_str():
    t = time.localtime(time.time())
    st = time.strftime('%Y-%m-%d %H:%M:%S', t)
    return st


def md5_encode(plain):
    """
    md5加密
    :param plain:待加密字符串
    :return: 密文
    """
    md = hashlib.md5()
    md.update(plain.encode('utf-8'))
    return md.hexdigest()


def md5_check(plain, cipher):
    """
    校验md5
    :param plain: 明文
    :param cipher: 密文
    :return: True or False
    """
    return md5_encode(plain) == cipher


def max_times(ite):
    dic = {}
    for i in ite:
        dic[i] = dic.get(i, 0) + 1
    return max(list(dic.values()))


def gen_random(length=2):
    """
    获取随机数
    :param length: 随机数长度
    :return: 随机数
    """
    o = ''
    for it in range(length):
        o += str(random.randint(0, 9))
    return o


def isAdmin(user):
    return user.role == 'ADMIN'


def get_desktop_path():
    """
    桌面路径
    :return:路径
    """
    if platform.system() == 'Windows':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0] + '\\'
    elif platform.system() == 'Linux':
        return '/home/'


if __name__ == '__main__':
    pwd = md5_encode('123')
    print(pwd)
