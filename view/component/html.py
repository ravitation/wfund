#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx.html


class HtmlShow(wx.html.HtmlWindow):
    def __init__(self, parent, ID, source=''):
        wx.html.HtmlWindow.__init__(self, parent, ID)
        if source:
            self.SetPage(source)

    def OnCellClicked(self, cell, x, y, event):
        print(cell)
        print(x,y)
        return True

    def OnLinkClicked(self, link):
        print(link)
        pass

    def OnCellMouseHover(self, cell, x, y):
        pass

    def OnOpeningURL(self, type, url):
        pass

    def OnSetTitle(self, title):
        pass

