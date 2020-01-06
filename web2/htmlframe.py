#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx.html2 import WebView
from web2.htmlwindow import HtmlWindow
from web2.htmldialog import HtmlDialog
from web2.page.index import cont


class HtmlFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(600, 500))
        # web_view = HtmlWindow.New(self)
        # web_view.LoadURL("https://baidu.com/")
        dlg = HtmlDialog(self)
        # dlg.browser.LoadURL("http://127.0.0.1:8848/web/explain/index.html")
        dlg.browser.SetPage(cont, "")
        dlg.Show()
