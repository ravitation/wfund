#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv


class DatePick(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID, size=(218, 240))
        self.date = adv.GenericCalendarCtrl(self, -1)
        # self.date = adv.GenericDatePickerCtrl(self, -1)
        button = wx.Button(self, wx.ID_OK, "Okay")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.date, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
