#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from view.component.datapick import DatePick
from model.fund import FundApply
from utils.util import now_time_str


class MaintainPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
        self.parent = parent

        topLbl = wx.StaticText(self, -1, 'New Apply')
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        nameLbl = wx.StaticText(self, -1, '申请人:')
        self.name = wx.TextCtrl(self, -1, "")
        kindLbl = wx.StaticText(self, -1, '类型:')
        self.kind = wx.TextCtrl(self, -1, "")
        dateLbl = wx.StaticText(self, -1, '日期:')
        self.date = wx.TextCtrl(self, -1, '')
        moneyLbl = wx.StaticText(self, -1, '金额:')
        self.money = wx.TextCtrl(self, -1, '')
        dscLbl = wx.StaticText(self, -1, '描述:')
        self.dsc = wx.TextCtrl(self, -1, '')

        calBtn = wx.Button(self, -1, '选择')
        self.Bind(wx.EVT_BUTTON, self.OnCalendarCtrl, calBtn)

        hLine = wx.StaticLine(self, wx.EXPAND)

        saveBtn = wx.Button(self, -1, '保存')
        self.Bind(wx.EVT_BUTTON, self.OnSaveApply, saveBtn)

        sizer = wx.GridBagSizer(vgap=5, hgap=5)
        sizer.Add(topLbl, pos=(0, 0), span=(1, 4), flag=wx.EXPAND)
        sizer.Add(nameLbl, pos=(1, 0), flag=wx.EXPAND)
        sizer.Add(self.name, pos=(1, 1), flag=wx.EXPAND)
        sizer.Add(kindLbl, pos=(1, 2), flag=wx.EXPAND)
        sizer.Add(self.kind, pos=(1, 3), flag=wx.EXPAND)
        sizer.Add(dateLbl, pos=(2, 0), flag=wx.EXPAND)
        dateSizer = wx.BoxSizer(wx.HORIZONTAL)
        dateSizer.Add(self.date, wx.EXPAND, border=1)
        dateSizer.Add(calBtn)
        sizer.Add(dateSizer, pos=(2, 1), flag=wx.EXPAND)
        sizer.Add(moneyLbl, pos=(2, 2), flag=wx.EXPAND)
        sizer.Add(self.money, pos=(2, 3), flag=wx.EXPAND)
        sizer.Add(dscLbl, pos=(3, 0), flag=wx.EXPAND)
        sizer.Add(self.dsc, pos=(3, 1), span=(1, 3), flag=wx.EXPAND)
        sizer.Add(hLine, pos=(4, 0), span=(1, 4), flag=wx.EXPAND)
        sizer.Add(saveBtn, pos=(5, 2), flag=wx.EXPAND)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)


    def OnCalendarCtrl(self, event):
        dlg = DatePick(self)
        if dlg.ShowModal() == wx.ID_OK:
            date = dlg.datepick.GetDate()
            s = date.Format('%Y-%m-%d')
            self.date.SetValue(s)

    def OnSaveApply(self, event):
        name = self.name.GetValue()
        kind = self.kind.GetValue()
        date = self.kind.GetValue()
        money = self.money.GetValue()
        dsc = self.dsc.GetValue()

        apply = FundApply(type=kind, state='', money=money, date=date, reason=dsc, persons='',
                          update_time=now_time_str(), create_time=now_time_str())
        apply.save()
        print(apply)
        print('save')
        self.parent.OnApplyFund(None)
