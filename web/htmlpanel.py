#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html
import os, sys
from web.html import WHtmlWindow
import urllib.request


class WHtmlPanel(wx.Panel):
    def __init__(self, parent, ID, frame, file=None):
        wx.Panel.__init__(self, parent, ID)
        self.frame = frame
        self.html = WHtmlWindow(self, -1, frame)
        self.html.SetRelatedFrame(self.frame, "%s")
        self.html.SetRelatedStatusBar(0)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.html, 1, wx.EXPAND)

        subbox = self.createHorBtn(self.btn_data())

        self.box.Add(subbox, 0, wx.EXPAND)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        if file.startswith("http://"):
            self.html.LoadPage(file)
        else:
            self.html.SetPage(file)

    def btn_data(self):
        return [('Load File', self.OnLoadFile),
                ('Load Page', self.OnLoadPage),
                ('Back', self.OnBack),
                ('Forward', self.OnForward)]

    def createHorBtn(self, btns):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in btns:
            btn = wx.Button(self, -1, item[0])
            self.Bind(wx.EVT_BUTTON, item[1], btn)
            sizer.Add(btn, 1, wx.EXPAND | wx.ALL, 2)
        return sizer

    def OnLoadPage(self, event):
        dlg = wx.TextEntryDialog(self, 'Location:')
        if dlg.ShowModal() == wx.ID_OK:
            self.destination = dlg.GetValue()
        dlg.Destroy()
        self.OpenUrl(self.destination)
        # self.html.LoadPage(self.destination)

    def OnLoadFile(self, event):
        dlg = wx.FileDialog(self, wildcard = '*.htm*', style=wx.FD_OPEN)
        if dlg.ShowModal():
            path = dlg.GetPath()
            self.html.LoadPage(path)
        dlg.Destroy()

    def OnBack(self, event):
        if not self.html.HistoryBack():
            wx.MessageBox("No more items in history!")

    def OnForward(self, event):
        if not self.html.HistoryForward():
            wx.MessageBox("No more items in history!")

    def OpenUrl(self, url):
        if str(url).startswith("http://"):
            pass
        else:
            url = "http://" + url
        page = str(urllib.request.urlopen(url).read(), "gb2312", "ignore").encode("utf-8", "ignore")
        print(page)
        self.html.SetPage(page)















