#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from model.fund import FundApply


class PerStatPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
        self.applies = FundApply.find()
        print(self.applies)
