#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid
from utils.compute import Compute
from model.common import User
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
        self.apply = FundApply.find(where="state='未报销'")
        self.all_user = User.all()

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

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(unuse_sizer, 1, wx.ALL, 5)
        h_sizer.Add(unpay_sizer, 1, wx.ALL, 5)

        self.grid = self.init_grid()

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        v_sizer.Add(h_sizer, 0, wx.ALL | wx.EXPAND, 5)
        v_sizer.Add(self.grid, 1, wx.ALL, 5)

        self.SetSizer(v_sizer)
        self.Layout()

    def init_grid(self):
        colLabels = ['时间', '操作', '金额（元）', '相关人员']
        grid = Part.GenGrid(self, colLabels, self.get_grid_data())
        grid.EnableEditing(False)
        return grid

    def get_grid_data(self):
        db_data = {}
        data = {}
        index = 0
        for item in self.provide:
            if item.user_id in self.all_user.keys():
                db_data[index] = (item.create_time, '增加', round(item.money, 2), self.all_user[item.user_id])
                index += 1

        for item in self.pay:
            if item.user_id in self.all_user.keys():
                db_data[index] = (item.create_time, '报销', round(item.money, 2), self.all_user[item.user_id])
                index += 1
        db_data = [k[1] for k in sorted(db_data.items(), key=lambda item: item[1], reverse=True)]
        for i in range(len(db_data)):
            item = db_data[i]
            for k in range(len(item)):
                data[(i, k)] = item[k]
        return data

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.init()
    pass

