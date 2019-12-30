#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from utils.validator import NotEmptyValidator
from model.common import User, Role
from utils.util import md5_encode, now_time_str


class Register(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID, size=(520, 220))
        self.roles = Role.all()

        codeLbl = wx.StaticText(self, -1, '用户名：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.code = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='code')
        pwdLbl = wx.StaticText(self, -1, '密码：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.pwd = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='pwd', style=wx.TE_PASSWORD)

        pwdSizer = wx.BoxSizer(wx.HORIZONTAL)
        pwdSizer.Add(codeLbl, 0, wx.ALL, 5)
        pwdSizer.Add(self.code, 1, wx.EXPAND | wx.ALL, 5)
        pwdSizer.Add(pwdLbl, 0, wx.ALL, 5)
        pwdSizer.Add(self.pwd, 1, wx.EXPAND | wx.ALL, 5)

        nameLbl = wx.StaticText(self, -1, '姓名：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.name = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='name')
        phoneLbl = wx.StaticText(self, -1, '电话：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.phone = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='phone')

        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(nameLbl, 0, wx.ALL, 5)
        nameSizer.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)
        nameSizer.Add(phoneLbl, 0, wx.ALL, 5)
        nameSizer.Add(self.phone, 1, wx.EXPAND | wx.ALL, 5)

        emailLbl = wx.StaticText(self, -1, '邮箱：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.email = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='email')
        roleLbl = wx.StaticText(self, -1, '角色：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.role = wx.Choice(self, -1, choices=[k for k in self.roles.values()])

        emailSizer = wx.BoxSizer(wx.HORIZONTAL)
        emailSizer.Add(emailLbl, 0, wx.ALL, 5)
        emailSizer.Add(self.email, 1, wx.EXPAND | wx.ALL, 5)
        emailSizer.Add(roleLbl, 0, wx.ALL, 5)
        emailSizer.Add(self.role, 1, wx.EXPAND | wx.ALL, 5)

        logBtn = wx.Button(self, wx.ID_OK, "保存")
        celBtn = wx.Button(self, wx.ID_CANCEL, "取消")
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(logBtn, 0, wx.ALL, 5)
        btnSizer.Add(celBtn, 0, wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnReg, logBtn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pwdSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(nameSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(emailSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.init()

    def init(self):
        self.role.SetSelection(1)
        pass

    def OnReg(self, event):
        code = self.code.GetValue()
        name = self.name.GetValue()
        password = self.pwd.GetValue()
        mobile = self.phone.GetValue()
        email = self.email.GetValue()
        index = self.role.GetSelection()
        role = [k for k in self.roles.keys()][index]
        users = User.find(where='code=?', args=code)
        if len(users) > 0:
            wx.MessageBox('用户已存在！', 'Error')
        else:
            user = User(code=code, name=name, password=md5_encode(password), mobile=mobile, email=email, role=role,
                        create_time=now_time_str(), update_time=now_time_str())
            user.save()
            dlg = wx.MessageDialog(None, 'Success!!', 'Message', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                self.EndModal(wx.ID_OK)
            dlg.Destroy()
