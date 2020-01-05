#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html
import os, sys
from web.htmlpanel import WHtmlPanel


class WHtmlFrame(wx.Frame):  # MDIParentFrame
    def __init__(self, parent, ID, title, file):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, size=(600, 550))
        self.CreateStatusBar()
        self.SetStatusText("Default status Bar")
        file = 'http://www.baidu.com' if not file else file
        panel = WHtmlPanel(self, -1, self, file)
        menu = wx.Menu()
        exit = menu.Append(-1, "E&xit", "Exit")
        new_window = menu.Append(-1, "N&ew Window", "New Window")
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "F&ile")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.Exit, exit)
        self.Bind(wx.EVT_MENU, self.OnNewWindow, new_window)

    def Exit(self, event):
        self.Close(True)

    def OnNewWindow(self, evt):
        win = wx.MDIChildFrame(self, -1, 'Mdi Child Window')
        panel = WHtmlPanel(win, -1, win, 'http://www.baidu.com')
        win.Show(True)

