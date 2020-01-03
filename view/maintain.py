#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from model.fund import FundApply, FundPayRecord
from model.common import User, Role
from model.fund import FundProvide
from utils.compute import Compute
from view.component.part import Part
from utils.util import now_time_str


class MaintainPanel(wx.Panel):
    def __init__(self, parent, ID, user=None):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
        self.parent = parent
        self.user = user

        self.title_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.default_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.init()

    def init(self):
        self.provide = FundProvide.find()
        self.pay = FundPayRecord.find()
        self.users = User.find()
        self.roles = Role.all()

        provide = Compute.zero()
        for item in self.provide:
            provide += item.money

        pay = Compute.zero()
        for item in self.pay:
            pay += item.money

        sy = provide - pay
        unuse = Part.GenShowText(self, round(sy, 2), self.default_font, wx.ALIGN_CENTER)
        add_btn = wx.Button(self, -1, '+', size=(25, 25), style=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnAddFund, add_btn)
        unuse_sizer = Part.GenStaticBoxSizer(self, '剩余（元）', [unuse, add_btn], wx.ALL, static_flags=wx.HORIZONTAL)

        self.grid = self.init_grid()

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        v_sizer.Add(unuse_sizer, 0, wx.ALL, 5)
        v_sizer.Add(self.grid, 1, wx.ALL, 5)
        self.SetSizer(v_sizer)
        self.Layout()

    def init_grid(self):
        colLabels = ['用户名', '姓名', '电话', '邮箱', '角色']
        self.grid_data = self.get_grid_data()
        print(self.grid_data)
        grid = Part.GenGrid(self, colLabels, {k: self.grid_data[k] for k in self.grid_data if k[1] != 5})
        grid.SetColSize(0, 175)
        grid.SetColSize(2, 200)
        grid.SetColSize(3, 200)
        grid.EnableEditing(False)
        return grid

    def get_grid_data(self):
        db_data = {}
        data = {}
        index = 0
        for item in self.users:
            db_data[index] = (item.code, item.name, item.mobile, item.email, self.roles[item.role],
                              item.id)
            index += 1

        for i in range(len(db_data)):
            item = db_data[i]
            for k in range(len(item)):
                data[(i, k)] = item[k]
        return data

    def OnAddFund(self, event):
        dlg = wx.TextEntryDialog(None, '输入金额：', '', '0.0',  style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            provide = FundProvide(money=dlg.GetValue(), create_time=now_time_str())
            provide.save()
            self.refresh(self.user)
        pass

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.init()
