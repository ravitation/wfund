#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from utils.compute import Compute
from model.fund import FundPayRecord, FundProvide, FundApply
from view.component.part import Part


class FundDetail(wx.Panel):
    def __init__(self, parent, ID, user=None):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
        self.title_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.default_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.user = user
        self.init()

    def init(self):
        self.provide = FundProvide.find()
        self.pay = FundPayRecord.find()
        self.apply = FundApply.find()

        provide = Compute.zero()
        for item in self.provide:
            provide += item.money

        pay = Compute.zero()
        for item in self.pay:
            pay += item.money

        apply = Compute.zero()
        for item in self.apply:
            apply += item.money

        sy = provide - pay
        sq = apply
        unuse = Part.GenShowText(self, round(sy, 2), self.default_font, wx.ALIGN_CENTER)
        unpay = Part.GenShowText(self, round(sq, 2), self.default_font, wx.ALIGN_CENTER)
        unuse_sizer = Part.GenStaticBoxSizer(self, '剩余（元）', [unuse], wx.ALL)
        unpay_sizer = Part.GenStaticBoxSizer(self, '未报销（元）', [unpay], wx.ALL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(unuse_sizer, 1, wx.ALL, 5)
        sizer.Add(unpay_sizer, 1, wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

        print(provide)
        print(pay)
        print(round(sy, 2))
        print(round(sq, 2))
        pass

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.init()
    pass

