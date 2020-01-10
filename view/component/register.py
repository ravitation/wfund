#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import os
import base64
from utils.validator import NotEmptyValidator
from model.common import User, Role
from utils.util import md5_encode, now_time_str
from utils.img_tran import EmbedImg


class Register(wx.Dialog):
    def __init__(self, parent, ID, user=None, user_id=None, admin=True):
        wx.Dialog.__init__(self, parent, ID, size=(520, 320))
        self.wildcard = "Picture files | *.JP*G|All files (* .*) | *.*"

        self.roles = Role.all()
        self.user = User()
        self.admin = admin
        if user_id:
            users = User.find(where='id=?', args=user_id)
            self.user = users[0] if users else self.user
        elif user:
            self.user = user

        if user_id:
            self.user_id = user_id

        codeLbl = wx.StaticText(self, -1, '用户名：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.code = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='code',
                                value=self.user.code if self.user else '')
        pwdLbl = wx.StaticText(self, -1, '密码：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.pwd = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='pwd', style=wx.TE_PASSWORD,
                               value=self.user.password if self.user else '')

        pwdSizer = wx.BoxSizer(wx.HORIZONTAL)
        pwdSizer.Add(codeLbl, 0, wx.ALL, 5)
        pwdSizer.Add(self.code, 1, wx.EXPAND | wx.ALL, 5)
        pwdSizer.Add(pwdLbl, 0, wx.ALL, 5)
        pwdSizer.Add(self.pwd, 1, wx.EXPAND | wx.ALL, 5)

        nameLbl = wx.StaticText(self, -1, '姓名：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.name = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='name',
                                value=self.user.name if self.user else '')
        phoneLbl = wx.StaticText(self, -1, '电话：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.phone = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='phone',
                                 value=self.user.mobile if self.user else '')

        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(nameLbl, 0, wx.ALL, 5)
        nameSizer.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)
        nameSizer.Add(phoneLbl, 0, wx.ALL, 5)
        nameSizer.Add(self.phone, 1, wx.EXPAND | wx.ALL, 5)

        emailSizer = wx.BoxSizer(wx.HORIZONTAL)
        emailLbl = wx.StaticText(self, -1, '邮箱：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.email = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='email',
                                 value=self.user.email if self.user else '')
        emailSizer.Add(emailLbl, 0, wx.ALL, 5)
        emailSizer.Add(self.email, 1, wx.EXPAND | wx.ALL, 5)
        if admin:
            roleLbl = wx.StaticText(self, -1, '角色：', size=(60, -1), style=wx.ALIGN_RIGHT)
            self.role = wx.Choice(self, -1, choices=[k for k in self.roles.values()])
            emailSizer.Add(roleLbl, 0, wx.ALL, 5)
            emailSizer.Add(self.role, 1, wx.EXPAND | wx.ALL, 5)

        picLbl = wx.StaticText(self, -1, '图片：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.pic = wx.StaticBitmap(self, -1, wx.Bitmap(60, 60), size=(60, 60))
        pic_btn = wx.Button(self, -1, '选择图片')

        self.picSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.picSizer.Add(picLbl, 0, wx.ALL, 5)
        self.picSizer.Add(self.pic, 0, wx.EXPAND | wx.ALL, 5)
        self.picSizer.Add(pic_btn, 0, wx.ALL, 5)
        self.pic64 = ''

        self.Bind(wx.EVT_BUTTON, self.OnChoicePic, pic_btn)

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
        sizer.Add(self.picSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.init_data()

    def init_data(self):
        if self.user:
            if self.admin:
                self.role.SetSelection(list(self.roles.keys()).index(self.user.role))
            if self.user.avatar:
                img = EmbedImg(self.user.avatar).GetImage()
                img.Rescale(60, 60)
                self.pic64 = wx.Bitmap(img)
                self.pic.SetBitmap(self.pic64)
                self.Layout()
        else:
            if self.admin:
                self.role.SetSelection(1)
        pass

    def OnChoicePic(self, event):
        dlg = wx.FileDialog(self, "Open Pic file...", os.getcwd(), style=wx.FD_OPEN, wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            with open(dlg.GetPath(), 'rb') as f:
                data = base64.b64encode(f.read())
                self.pic64 = data
                img = EmbedImg(data).GetImage()
                img.Rescale(60, 60)
                self.pic.SetBitmap(wx.Bitmap(img))
                self.Layout()
        dlg.Destroy()

    def OnReg(self, event):
        code = self.code.GetValue()
        name = self.name.GetValue()
        password = self.pwd.GetValue()
        mobile = self.phone.GetValue()
        email = self.email.GetValue()
        users = User.find(where='code=?', args=code)
        if len(users) > 0 and not self.user:
            wx.MessageBox('用户已存在！', 'Error')
        else:
            if self.user and password == self.user.password:
                pass
            else:
                password = md5_encode(password)

            if self.user:
                role = self.user.role
                user = User(id=self.user.id, code=code, name=name, password=password, mobile=mobile, email=email,
                            role=role, create_time=now_time_str(), update_time=now_time_str(), avatar=self.pic64)
                user.update()
            else:
                index = self.role.GetSelection()
                role = [k for k in self.roles.keys()][index]
                user = User(code=code, name=name, password=password, mobile=mobile, email=email, role=role,
                            create_time=now_time_str(), update_time=now_time_str(), avatar=self.pic64)
                user.save()
            dlg = wx.MessageDialog(None, 'Success!!', 'Message', wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                self.EndModal(wx.ID_OK)
            dlg.Destroy()
