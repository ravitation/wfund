#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import math


class CheckBox(wx.Dialog):
    def __init__(self, parent, ID, title='选择窗口', checks=None, defaults=None, columns=5):
        wx.Dialog.__init__(self, parent, ID, size=(450, 260))
        button = wx.Button(self, wx.ID_OK, "确认")
        self.SetTitle(title)
        self.columns = columns
        self.rows = 0
        self.checked = []
        if checks:
            self.checks = checks
        if defaults:
            self.defaults = defaults

        self.compute()
        self.ch_panel = self.create_box()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ch_panel, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

    def create_box(self):
        panel = wx.Panel(self, -1)
        flexSizer = wx.FlexGridSizer(cols=self.columns, rows=self.rows, hgap=5, vgap=5)
        for item in self.checks:
            c = wx.CheckBox(panel, -1, item)
            for d in self.defaults:
                if d == item:
                    c.SetValue(True)
                    self.checked.append(item)
            self.Bind(wx.EVT_CHECKBOX, self.OnCheck, c)
            flexSizer.Add(c, 0, wx.ALL, 5)
        panel.SetSizer(flexSizer)
        panel.Layout()
        return panel

    def OnCheck(self, event):
        cb = event.GetEventObject()
        if cb.IsChecked():
            self.checked.append(cb.GetLabel())
        else:
            self.checked.remove(cb.GetLabel())

    def compute(self):
        num = len(self.checks)
        if num < self.columns:
            self.rows = 1
        else:
            self.rows = math.ceil(num / self.columns)
