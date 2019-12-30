#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv


class DatePick(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, '日期选择')
        ok = wx.Button(self, wx.ID_OK, "确认")
        cancel = wx.Button(self, wx.ID_CANCEL, "取消")
        self.datepick = adv.CalendarCtrl(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.datepick, 1, wx.EXPAND | wx.ALL, 5)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(ok, 0, wx.ALL, 5)
        btnSizer.Add(cancel, 0, wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)
        self.Layout()
