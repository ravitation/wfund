#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import xlwt
import math
import datetime
from wx import adv
from model.common import User, Role
from model.fund import FundApply, FundPayRecord, FundKind
from utils.util import get_desktop_path, isAdmin
from utils.compute import Compute
from view.component.part import Part


class GenSheet(wx.Dialog):
    cols = ['日期', '报账人', '金额(元)', '类型', '描述', '状态', '人员']
    lens = [100, 100, 80, 50, 320, 50, 320]

    def __init__(self, parent, ID, user=None):
        wx.Dialog.__init__(self, parent, ID, size=(520, 360))
        self.SetTitle("生成表单")
        self.user = user
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.init()
        self.SetSizer(self.sizer)
        self.Layout()

    def init(self):
        self.user_map = User.all()
        self.kinds = FundKind.all()
        self.init_data()
        self.common()
        if isAdmin(self.user):
            self.admin_sheet()
        else:
            self.user_sheet()

    def init_data(self):
        self.states = ['未报销']
        self.apply_ids = [str(k) for k in self.user_map]
        now = datetime.datetime.now()
        self.dates = {'begin': now.strftime('%Y-%m-%d'), 'end': now.strftime('%Y-%m-%d')}
        pass

    def common(self):
        begin_label = wx.StaticText(self, -1, '开始时间：')
        begin = adv.GenericDatePickerCtrl(self, -1, name='begin')

        end_label = wx.StaticText(self, -1, '结术时间：')
        end = adv.GenericDatePickerCtrl(self, -1)
        for date in [begin, end]:
            self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChange, date)
        date_sizer = Part.GenStaticBoxSizer(self, '报销状态', [begin_label, begin, end_label, end], static_flags=wx.HORIZONTAL)
        self.sizer.Add(date_sizer, 0, wx.ALL, 5)

        unpay_btn = wx.CheckBox(self, -1, "未报销")
        hadpay_btn = wx.CheckBox(self, -1, "已报销")
        unpay_btn.SetValue(True)
        for btn in [unpay_btn, hadpay_btn]:
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckState, btn)
        state_sizer = Part.GenStaticBoxSizer(self, '报销状态', [unpay_btn, hadpay_btn], static_flags=wx.HORIZONTAL)
        self.sizer.Add(state_sizer, 0, wx.ALL, 5)
        pass

    def admin_sheet(self):
        checks = []
        self.user_checks =[]
        self.columns = 6
        self.rows = 0
        self.compute(self.user_map)
        flexSizer = wx.FlexGridSizer(cols=self.columns, rows=self.rows, hgap=5, vgap=5)
        for key in self.user_map:
            value = self.user_map[key]
            check = wx.CheckBox(self, -1, value, name=str(key))
            checks.append(check)
            check.SetValue(True)
            self.user_checks.append(check)
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckPeople, check)
            flexSizer.Add(check, 0, wx.ALL, 5)
        all_btn = wx.Button(self, -1, '全选/全不选', name='all')
        self.Bind(wx.EVT_BUTTON, self.OnCheckPeople, all_btn)
        flexSizer.Add(all_btn, 0, wx.ALL, 5)
        static_sizer = Part.GenStaticBoxSizer(self, '人员', [flexSizer], static_flags=wx.HORIZONTAL)
        self.sizer.Add(static_sizer, 0, wx.ALL | wx.EXPAND, 5)

        btn = wx.Button(self, -1, '生成')
        self.Bind(wx.EVT_BUTTON, self.OnGenSheet, btn)
        self.sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        pass

    def user_sheet(self):
        print("user")
        pass

    def OnCheckState(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if obj.IsChecked():
            if state not in self.states:
                self.states.append(state)
        else:
            self.states.remove(state)

    def OnCheckPeople(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if name == 'all':
            if len(self.apply_ids) != len(self.user_map):
                for check in self.user_checks:
                    check.SetValue(True)
                self.apply_ids = [str(k) for k in self.user_map]
            elif len(self.apply_ids) == len(self.user_map):
                for check in self.user_checks:
                    check.SetValue(False)
                self.apply_ids = []
            pass
        else:
            if obj.IsChecked():
                self.apply_ids.append(name)
            else:
                self.apply_ids.remove(name)

    def OnDateChange(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        dt = obj.GetValue()
        df = dt.Format('%Y-%m-%d')
        if name == 'begin':
            self.dates['begin'] = df
        else:
            self.dates['end'] = df

    def OnGenSheet(self, event):
        sheet_data = self.get_sheet_data()
        path = get_desktop_path() + '经费申请_' + self.user.name + '.xls'
        file = xlwt.Workbook()
        table = file.add_sheet('经费申请',
                               cell_overwrite_ok=True)
        for j in range(len(GenSheet.lens)):
            table.col(j).width = GenSheet.lens[j] * 35
        row = 0
        for col in range(len(GenSheet.cols)):
            table.write(row, col, GenSheet.cols[col])
        row = row + 1
        for item in sheet_data:
            for col in range(len(item)):
                table.write(row, col, item[col])
            row = row + 1

        file.save(path)
        pass

    def get_sheet_data(self):
        ids = ''
        states = ''
        for id in self.apply_ids:
            ids += "user_id='" + id + "' or "
        ids = ids[:-3]
        for state in self.states:
            states += "state='" + state + "' or "
        states = states[:-3]
        applies = FundApply.find(where="(" + ids + ")" + " and (" + states + ")")
        sheet_data = []
        applies = sorted(applies, key=lambda key: key['date'])
        for apply in applies:
            item = []
            try:
                dt = wx.DateTime(datetime.datetime.strptime(apply.date, '%Y年%m月%d日'))
            except ValueError:
                dt = wx.DateTime(datetime.datetime.strptime(apply.date, '%Y-%m-%d'))
            df = dt.Format('%Y-%m-%d')
            if self.dates['begin'] < df < self.dates['end']:
                item.append(apply.date)
                item.append(self.user_map[apply.user_id])
                item.append(Compute.get(apply.money))
                item.append(self.kinds[apply.kind])
                item.append(apply.reason)
                item.append(apply.state)
                item.append(apply.persons)
                sheet_data.append(tuple(item))
        return sheet_data

    def compute(self, checks):
        num = len(checks)
        if num < self.columns:
            self.rows = 1
        else:
            self.rows = math.ceil(num / self.columns)


