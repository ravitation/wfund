#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid
from model.fund import FundApply, FundKind
from model.common import User
from utils.compute import Compute
from view.component.part import Part


class ClsStatPanel(wx.Panel):
    def __init__(self, parent, ID, user=None):
        wx.Panel.__init__(self, parent, ID)

        self.title_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.default_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.SetBackgroundColour('White')
        self.user = user

        self.init()

    def init(self):
        self.show()
        self.createPopupMenu()

    def show(self):
        self.applies = FundApply.find(where="state='未报销'")
        self.fund_kind = FundKind.all()
        self.users = User.all()
        self.money_dict = self.all_money(self.applies)

        all = Part.GenShowText(self, round(self.money_dict['all'], 2), self.default_font, wx.ALIGN_CENTER)
        allSizer = Part.GenStaticBoxSizer(self, '总计（元）', [all], wx.ALL | wx.EXPAND)

        self.grid = self.init_grid()

        sizer = wx.BoxSizer(wx.VERTICAL)
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
        colLabels = ['人员', self.fund_kind['01'], self.fund_kind['02'], self.fund_kind['03'], self.fund_kind['04']]
        print(colLabels)
        grid = Part.GenGrid(self, colLabels, self.get_grid_data())
        grid.EnableEditing(False)
        return grid

    def get_grid_data(self):
        db_data = {}
        data = {}
        for item in self.applies:
            if item.user_id in db_data.keys():
                db_data[item.user_id].append(item)
            else:
                db_data[item.user_id] = [item]

        row = 0
        for k in db_data:
            items = db_data[k]
            dic = self.all_money(items)
            data[(row, 0)] = self.users[k]
            for i in dic:
                col = 0
                key = ()
                if i == 'meal': key = (row, (col + 1))
                if i == 'taxi': key = (row, (col + 2))
                if i == 'oil': key = (row, (col + 3))
                if i == 'other': key = (row, (col + 4))
                if i != 'all': data[key] = str(round(dic[i]['money'], 2))
                col += 1
            row += 1
        print(data)
        return data

    def menuData(self):
        return [("报销", "", self.OnPopupPaySelected, '')]

    def createPopupMenu(self):
        self.popupmenu = wx.Menu()
        self.popupmenu = Part.CreateMenu(self, self.menuData())
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnShowPopup, self.grid)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        self.select_grid_row = event.GetRow()
        self.grid.PopupMenu(self.popupmenu, pos)

    def OnPopupPaySelected(self, event):
        col_nums = self.grid.GetTable().GetNumberCols()
        pay = Compute.zero()
        for i in range(1, col_nums):
            print(i)
            pay += Compute.parse(self.grid.GetTable().GetDataValue(self.select_grid_row, i))
            pass
        applyId = self.grid.GetTable().GetDataValue(self.select_grid_row, 1)
        print(applyId)

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.show()
