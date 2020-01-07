#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx


class GenIdCard(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
        btn = wx.Button(self, -1, 'Button')


class Frame(wx.Frame):
    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID)
        panel = GenIdCard(self, -1)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(panel, 1, wx.EXPAND)
        hbox.Layout()
        self.SetSizer(hbox)


if __name__ == '__main__':
    app = wx.App()
    frame = Frame(None, -1)
    frame.Center()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
    pass

