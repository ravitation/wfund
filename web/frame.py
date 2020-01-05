#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html as html
import urllib.request


class MainFrame(wx.MDIParentFrame):
    def __init__(self, parent, ID, title=u'MDI'):
        wx.MDIParentFrame.__init__(self, parent, ID, title, size=(700, 600))
        self.textCtrl = wx.TextCtrl(self, -1, "", pos=(10, 10), size=(400, 30))
        self.textCtrl.Bind(wx.EVT_TEXT, self.OnTextChange)
        self.textCtrl.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.button = wx.Button(self, -1, "OK", pos=(430, 10), size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)
        self.win = html.HtmlWindow(self, -1, style=wx.NO_BORDER, pos=(10, 50), size=(700, 700))
        self.url = ""

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.OpenUrl()
        event.Skip()

    def OnTextChange(self, evt):
        pass

    def OnButtonClick(self, evt):
        self.OpenUrl()

    def OpenUrl(self):
        self.url = self.textCtrl.GetValue()
        if str(self.url).startswith("http://"):
            pass
        else:
            self.url = "http://" + self.url

        page = str(urllib.request.urlopen(self.url).read(), "gb2312", "ignore").encode("utf-8", "ignore")
        print(page)
        self.win.SetPage(page)

