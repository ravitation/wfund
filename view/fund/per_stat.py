#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from model.fund import FundApply
from utils.compute import Compute
from model.fund import FundKind
from view.component.part import Part


class PerStatPanel(wx.Panel):
    def __init__(self, parent, ID, user=None):
        wx.Panel.__init__(self, parent, ID)

        self.title_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.default_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.SetBackgroundColour('White')
        self.user = user
        self.show()

    def show(self):
        self.applies = FundApply.find(where="user_id=? and state='未报销'", args=self.user.id)
        self.fund_kind = FundKind.all()

        self.money_dict = self.all_money(self.applies)
        # title = Part.GenShowText(self, '个人统计', self.title_font, style=wx.ALIGN_CENTER)
        # h_line = wx.StaticLine(self, -1)

        all = Part.GenShowText(self, round(self.money_dict['all'], 2), self.default_font, wx.ALIGN_CENTER)
        allSizer = Part.GenStaticBoxSizer(self, '总计（元）', [all], wx.ALL | wx.EXPAND)

        self.grid = self.init_grid()

        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(title, 0, wx.EXPAND | wx.ALL, 5)
        # sizer.Add(h_line, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(allSizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.show_detail(), 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

    def all_money(self, applies):
        total = Compute.zero()
        dic = {}
        for apply in applies:
            total += apply.money
            if apply.kind == '01':
                if 'meal' in dic.keys():
                    dic['meal']['money'] = dic['meal']['money'] + apply.money
                else:
                    dic['meal'] = {'name': self.fund_kind[apply.kind] + '（元）', 'money': apply.money}
            if apply.kind == '03':
                if 'oil' in dic.keys():
                    dic['oil']['money'] = dic['oil']['money'] + apply.money
                else:
                    dic['oil'] = {'name': self.fund_kind[apply.kind] + '（元）', 'money': apply.money}
            if apply.kind == '02':
                if 'taxi' in dic.keys():
                    dic['taxi']['money'] = dic['taxi']['money'] + apply.money
                else:
                    dic['taxi'] = {'name': self.fund_kind[apply.kind] + '（元）', 'money': apply.money}
            if apply.kind == '04':
                if 'other' in dic.keys():
                    dic['other']['money'] = dic['other']['money'] + apply.money
                else:
                    dic['other'] = {'name': self.fund_kind[apply.kind] + '（元）', 'money': apply.money}
        dic['all'] = total
        return dic

    def show_detail(self):
        items = self.money_dict
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for k in self.money_dict:
            if k != 'all':
                txt = Part.GenShowText(self, round(items[k]['money'], 2), self.default_font, wx.ALIGN_CENTER)
                sizer = Part.GenStaticBoxSizer(self, items[k]['name'], [txt], wx.ALL | wx.EXPAND)
                h_sizer.Add(sizer, 1, wx.ALL, 5)
        return h_sizer

    def init_grid(self):
        colLabels = ['日期', '类型', '金额（元）', '相关人员']
        grid = Part.GenGrid(self, colLabels, self.get_grid_data())
        grid.EnableEditing(False)
        return grid

    def get_grid_data(self):
        db_data = {}
        data = {}
        index = 0
        for item in self.applies:
            db_data[index] = (item.date, self.fund_kind[item.kind], round(item.money), item.persons, item.id)
            index += 1

        for i in range(len(db_data)):
            item = db_data[i]
            for k in range(len(item)):
                if k < 4: data[(i, k)] = item[k]
        return data

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.show()
