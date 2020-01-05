#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from web2.htmlwindow import HtmlWindow


class HtmlDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, '关于 WFund', size=(440, 260))
        self.init()

    def init(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = HtmlWindow.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((700, 700))

