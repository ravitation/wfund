#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from web2.htmlwindow import HtmlWindow


class HtmlPanel(wx.Panel):
    def __init__(self, parent, ID, frame, file=None):
        wx.Panel.__init__(self, parent, ID, size=(500, 500))
        web_view = HtmlWindow.New(self)
        web_view.LoadURL("https://baidu.com/")


