#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from utils.img_tran import EmbedImg
from view.component.register import Register


class UserInfo(wx.Panel):
    def __init__(self, parent, ID, user=None):
        wx.Panel.__init__(self, parent, ID)
        self.wildcard = "Picture files | *.JP*G|All files (* .*) | *.*"
        self.SetBackgroundColour('White')
        self.name_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.default_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.user = user
        self.init()

    def init(self):
        self.show()
        pass

    def user_data(self):
        return [('姓名：', self.user.name), ('电话：', self.user.mobile),
                ('邮箱：', self.user.email)]

    def userinfo(self):
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        for item in self.user_data():
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, -1, item[0])
            val = wx.StaticText(self, -1, item[1])
            h_sizer.Add(label, 0, wx.ALL, 5)
            h_sizer.Add(val, 0, wx.ALL, 5)
            v_sizer.Add(h_sizer, 0, wx.ALL, 5)
        return v_sizer

    def show(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        v_sizer = self.userinfo()
        btn = wx.Button(self, -1, '修改信息')
        v_sizer.Add(btn, 0, wx.ALL | wx.EXPAND, 5)
        self.Bind(wx.EVT_BUTTON, self.OnEditUserInfo, btn)

        if self.user.avatar:
            bmp = EmbedImg(self.user.avatar).GetImage()
            bmp.Rescale(120, 120)
        else:
            bmp = wx.Image(120, 120)

        pic_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avatar = wx.StaticBitmap(self, -1, wx.Bitmap(bmp), style=wx.BORDER)
        pic_sizer.Add(self.avatar, 0, wx.ALL, 5)

        sizer.Add(pic_sizer, 0, wx.ALL, 5)
        sizer.Add(v_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnEditUserInfo(self, event):
        reg = Register(self, -1, user=self.user, admin=False)
        if reg.ShowModal() == wx.ID_OK:
            wx.MessageBox('修改成功，下次启动生效！')

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.init()
