#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid
from model.fund import FundApply, FundKind, FundPayRecord
from model.common import User
from utils.compute import Compute
from utils.util import now_time_str
from utils.email import Email
from view.component.part import Part
from config.config import mail_template


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
        colLabels = ['人员', self.fund_kind['01'] + '（元）', self.fund_kind['02'] + '（元）',
                     self.fund_kind['03'] + '（元）', self.fund_kind['04'] + '（元）', '总计（元）']
        self.grid_data = self.get_grid_data()
        grid = Part.GenGrid(self, colLabels, self.get_grid_data())
        grid.EnableEditing(False)
        # grid.SetDefaultCellOverflow(False)

        grid.SetColSize(0, 110)
        grid.SetColSize(1, 125)
        grid.SetColSize(2, 125)
        grid.SetColSize(3, 125)
        grid.SetColSize(4, 125)
        grid.SetColSize(5, 125)
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
            print(dic)
            data[(row, 0)] = self.users[k]
            data[(row, 6)] = k
            for i in dic:
                col = 0
                key = ()
                if i == 'meal': key = (row, 1)
                if i == 'taxi': key = (row, 2)
                if i == 'oil': key = (row, 3)
                if i == 'other': key = (row, 4)
                if i != 'all': data[key] = str(round(dic[i]['money'], 2))
                if i == 'all':
                    key = (row, col + 5)
                    data[key] = str(round(dic[i], 2))
                col += 1
            row += 1
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
        pay = Compute.parse(self.grid.GetTable().GetDataValue(self.select_grid_row, 5))
        user_id = self.grid_data.get((self.select_grid_row, 6))
        dlg = wx.MessageDialog(None, '此操作将清空此用户申请信息!', '提示', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            if round(pay, 2) > 0 and user_id:
                fund_pay = FundPayRecord(money=pay, user_id=user_id, create_time=now_time_str())
                fund_pay.save()
                self.send_email(user_id)
                applies = FundApply.find(where='user_id=?', args=user_id)
                if applies and len(applies) > 0:
                    for apply in applies:
                        apply['state'] = '已报销'
                        apply.update()
            self.refresh(self.user)
        event.Skip()
        dlg.Destroy()

    def send_email(self, user_id):
        users = User.find(where='id=?', args=user_id)
        paies = (self.grid_data.get((self.select_grid_row, 1)) or 0,
                 self.grid_data.get((self.select_grid_row, 2)) or 0,
                 self.grid_data.get((self.select_grid_row, 3)) or 0,
                 self.grid_data.get((self.select_grid_row, 4)) or 0,
                 self.grid_data.get((self.select_grid_row, 5)))
        if len(users) > 0:
            user = users[0]
            sender = (user.name, user.email)
            cont = mail_template % (sender[0], paies[4], paies[0], paies[1], paies[2], paies[3])
            Email(cont, None, None, sender[1], subject='经费报销', sender_text='', to_text=sender[0]).send()
        pass

    def refresh(self, user):
        self.user = user
        self.DestroyChildren()
        self.show()
