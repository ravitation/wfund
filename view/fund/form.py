#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv
from view.component.check_dialog import CheckBox
from model.common import User
from model.fund import FundKind, FundApply
from utils.validator import NotEmptyValidator
from utils.util import now_time_str


class Form(wx.Dialog):
    def __init__(self, parent, ID, user=None, title='新增'):
        wx.Dialog.__init__(self, parent, ID, size=(420, 300))
        self.SetTitle(title)
        self.data = {}
        self.kinds = FundKind.all()
        self.allPersons = User.all()
        self.user = user

        self.nameLbl = wx.StaticText(self, -1, '姓名：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.name = wx.TextCtrl(self, -1, validator=NotEmptyValidator(), name='name', value=self.user.name)
        self.kindLbl = wx.StaticText(self, -1, '类型：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.kind = wx.Choice(self, -1, choices=[k for k in self.kinds.values()])
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer.Add(self.nameLbl, wx.ALL, 5)
        nameSizer.Add(self.name, wx.ALL | wx.EXPAND, 5)
        nameSizer.Add(self.kindLbl, wx.ALL, 5)
        nameSizer.Add(self.kind, wx.ALL | wx.EXPAND, 5)

        self.name.Bind(wx.EVT_KILL_FOCUS, self.OnNameEnter)
        self.kind.Bind(wx.EVT_CHOICE, self.OnChoiceKind)

        self.dateLbl = wx.StaticText(self, -1, '日期：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.date = adv.GenericDatePickerCtrl(self, -1)
        self.moneyLbl = wx.StaticText(self, -1, '金额：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.money = wx.TextCtrl(self, -1, name='money', validator=NotEmptyValidator())
        dateSizer = wx.BoxSizer(wx.HORIZONTAL)
        dateSizer.Add(self.moneyLbl, wx.ALL, 5)
        dateSizer.Add(self.money, wx.EXPAND | wx.ALL, 5)
        dateSizer.Add(self.dateLbl, wx.ALL, 5)
        dateSizer.Add(self.date, wx.EXPAND | wx.ALL, 5)

        self.money.Bind(wx.EVT_KILL_FOCUS, self.OnNameEnter)

        self.expLbl = wx.StaticText(self, -1, '描述：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.reason = wx.TextCtrl(self, -1, name='reason', size=(200, 80), style=wx.TE_MULTILINE,
                                  validator=NotEmptyValidator())
        expSizer = wx.BoxSizer(wx.HORIZONTAL)
        expSizer.Add(self.expLbl, wx.ALL, 5)
        expSizer.Add(self.reason, wx.EXPAND|wx.ALL, 5)

        self.reason.Bind(wx.EVT_KILL_FOCUS, self.OnNameEnter)

        self.peopleLbl = wx.StaticText(self, -1, '人员：', size=(60, -1), style=wx.ALIGN_RIGHT)
        self.persons = wx.StaticText(self, -1)
        self.peopleBtn = wx.Button(self, -1, '选择')
        self.Bind(wx.EVT_BUTTON, self.OnCheckPeople, self.peopleBtn)

        peopleSizer = wx.BoxSizer(wx.HORIZONTAL)
        peopleSizer.Add(self.peopleLbl, wx.ALL, 5)
        peopleSizer.Add(self.persons, wx.ALL|wx.EXPAND, 5)
        peopleSizer.Add(self.peopleBtn, wx.ALL, 5)

        okBtn = wx.Button(self, wx.ID_OK, "保存")
        cancelBtn = wx.Button(self, wx.ID_CANCEL, "取消")
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnSave, okBtn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nameSizer, 0, wx.ALL, 5)
        sizer.Add(dateSizer, 0, wx.ALL, 5)
        sizer.Add(expSizer, 0, wx.ALL, 5)
        sizer.Add(peopleSizer, 0, wx.ALL, 5)
        sizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.init_data()

    def init_data(self):
        dt = self.date.GetValue()
        df = dt.Format('%Y年%m月%d日')
        self.data.setdefault('date', df)

        self.persons.SetLabel(self.user.name)
        self.data.setdefault('persons', self.persons.GetLabel())

        self.kind.SetSelection(0)
        self.data.setdefault('kind', [k for k in self.kinds.keys()][self.kind.GetSelection()])

        self.data.setdefault('persons', self.persons.GetLabel())

    def OnCheckPeople(self, event):
        self.check = CheckBox(self, -1, checks=[k for k in self.allPersons.values()], defaults=self.persons.GetLabel().split(' '))
        if self.check.ShowModal() == wx.ID_OK:
            persons = ' '.join(self.check.checked)
            self.persons.SetLabel(' '.join(self.check.checked))
            self.data['persons'] = persons

    def OnNameEnter(self, event):
        eo = event.GetEventObject()
        self.data[eo.GetName()] = eo.GetValue()
        event.Skip()

    def OnChoiceKind(self, event):
        eo = event.GetEventObject()
        self.data['kind'] = [k for k in self.kinds.keys()][eo.GetSelection()]

    def OnSave(self, event):
        apply = FundApply(user_id=self.user.id, state='未报销', create_time=now_time_str(), update_time=now_time_str(),
                          **self.data)
        apply.save()
        wx.MessageBox('保存成功！', 'Error')
        self.EndModal(wx.ID_OK)


