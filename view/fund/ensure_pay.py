#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from model.common import User
import wx.html
from utils.img_tran import EmbedImg


class EnsurePay(wx.Dialog):
    def __init__(self, parent, user_id, money):
        wx.Dialog.__init__(self, parent, -1, '关于 WFund', size=(440, 260))
        self.font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.user = User.find_by_key(user_id)
        ok = wx.Button(self, wx.ID_OK, "确认")
        cancel = wx.Button(self, wx.ID_CANCEL, "取消")
        btn_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_Sizer.Add(ok, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        btn_Sizer.Add(cancel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        text = wx.StaticText(self, -1, '申请人：%s\n\n金额：%s' % (self.user.name, money), style=wx.NORMAL)
        text.SetFont(self.font)
        if self.user.avatar:
            bmp = EmbedImg(self.user.avatar).GetImage()
            bmp.Rescale(120, 120)
        else:
            bmp = wx.Image(120, 120)

        pic_sizer = wx.BoxSizer(wx.VERTICAL)
        self.avatar = wx.StaticBitmap(self, -1, wx.Bitmap(bmp), style=wx.BORDER)
        pic_sizer.Add(self.avatar, 0, wx.ALL, 5)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(pic_sizer, 0, wx.ALL, 5)
        h_sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer.Add(btn_Sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

