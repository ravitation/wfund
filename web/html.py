#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html
import os, sys


class WHtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, ID, frame):
        wx.html.HtmlWindow.__init__(self, parent, ID)

    def OnCellClicked(self, cell, x, y, event):
        print()
        print(x,y)
        return True

    def OnLinkClicked(self, link):
        print(link)
        pass

    def OnCellMouseHover(self, cell, x, y):
        # print(cell)
        # print(x, y)
        pass

    def OnOpeningURL(self, type, url):
        print(type)
        print(url)
        pass

    def OnSetTitle(self, title):
        pass

