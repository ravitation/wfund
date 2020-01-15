#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import os
from utils.validator import NotEmptyValidator
from model.common import User
from utils.util import md5_check


class Login(wx.Dialog):
    def __init__(self, parent, ID):
        self.log_user = None
        wx.Dialog.__init__(self, parent, ID, size=(220, 180))

        nameLbl = wx.StaticText(self, -1, '姓名：', size=(50, -1), style=wx.ALIGN_RIGHT)
        self.name = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='name')
        self.Center()

        nameSizer  = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(nameLbl, 0, wx.ALL, 5)
        nameSizer.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)

        pwdLbl = wx.StaticText(self, -1, '密码：', size=(50, -1), style=wx.ALIGN_RIGHT)
        self.pwd = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='pwd', style=wx.TE_PASSWORD)

        pwdSizer = wx.BoxSizer(wx.HORIZONTAL)
        pwdSizer.Add(pwdLbl, 0, wx.ALL, 5)
        pwdSizer.Add(self.pwd, 1, wx.EXPAND | wx.ALL, 5)

        logBtn = wx.Button(self, wx.ID_OK, "登录")
        celBtn = wx.Button(self, wx.ID_CANCEL, "取消")
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(logBtn, 0, wx.ALL, 5)
        btnSizer.Add(celBtn, 0, wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnLog, logBtn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nameSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(pwdSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.directLog()

    def directLog(self):
        sys_name = os.getlogin()
        users = User.find(where='code=?', args=sys_name)
        if users:
            user = users[0]
            if user and md5_check(sys_name, user.password):
                self.log_user = user
            else:
                wx.MessageBox('初始化密码错误，登录失败！', 'Error')
        else:
            wx.MessageBox('用户不存在, 请使用用户名和密码登录！', 'Error')

    def OnLog(self, event):
        code = self.name.GetValue()
        pwd = self.pwd.GetValue()
        users = User.find(where='code=?', args=code)
        if users:
            user = users[0]
            if user and md5_check(pwd, user.password):
                self.log_user = user
                self.EndModal(wx.ID_OK)
            else:
                wx.MessageBox('密码错误，登录失败！', 'Error')
        else:
            wx.MessageBox('用户不存在！', 'Error')


