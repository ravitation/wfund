#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import time
import importlib
from utils.menu import Menu
from view.about import WFundAbout
from view.maintain import MaintainPanel
from view.per_stat import PerStatPanel
from view.component.login import Login
from view.component.register import Register
from view.fund.form import Form
from model.common import Config
from config.data import icon
from config.img import EmbedImg


class WFundFrame(wx.Frame):
    def __init__(self, parent, pid):
        self.user = None
        self.title = "WFund - Give me Five"
        wx.Frame.__init__(self, parent, pid, self.title, size=(800, 600))
        ico = EmbedImg(icon).GetIcon()
        self.SetIcon(ico)
        self.filename = ''
        self.wildcard = "WFund files (*.WFund) | *.WFund|All files (* .*) | *.*"
        self.panel_list = []
        self.SetBackgroundColour('White')

        self.login()
        self.initStatusBar()
        self.initMenu()
        self.createPanel()

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -3, -2])
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def menuData(self):
        return [("操作", (
            ("新增申请\tCtrl+N", "", self.OnApplyFund, 'N'),
            ("个人统计\tCtrl+P", "", self.OnPerStat, 'P'),
            ("组内统计\tCtrl+G", "", self.OnClsStat, 'G'),
            ("详情\tCtrl+D", "", self.OnDetail, 'D'),
            ("", "", "", ''),
            ("维护\tCtrl+M", "", self.OnMaintain, 'M'),
            ("申请开关", (
                ("开\tCtrl+Alt+O", "", self.OnApplySign, 'O', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
                ("关\tCtrl+Alt+C", "", self.OnApplySign, 'C', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
            )),
            ("", "", "", ''),
            ("关闭\tCtrl+Q", "", self.OnCloseWindow, 'Q')),
         ), ("帮助", (
             ("&关于\tCtrl+Shift+A", "", self.OnAbout, 'A', wx.ACCEL_CTRL | wx.ACCEL_SHIFT),
             ("&说明\tCtrl+E", "", self.OnAbout, 'E')
         ))]

    def initMenu(self):
        self.menu = Menu(self, self.menuData())
        signs = Config.find(where='code=? and sign=\'Y\'', args='applySign')
        if signs:
            val = signs[0].value
            if val == 'N':
                id = self.menu.FindMenuItem('操作', '关')
                apply_menu = self.menu.FindItemById(id)
                if apply_menu.IsCheckable():
                    # apply_menu.IsChecked()
                    apply_menu.Check(True)

                pass


    def createPanel(self):
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hbox)
        self.OnPerStat(None)

    def OnApplyFund(self, event):
        self.form = Form(self, -1, user=self.user)
        if self.form.ShowModal() == wx.ID_OK:
            print(self.form.data)
        # self.apply_panel = None
        # self.changePanel('view.apply', 'ApplyPanel', self.apply_panel)

    def OnPerStat(self, event):
        self.per_stat_panel = None
        self.changePanel('view.per_stat', 'PerStatPanel', self.per_stat_panel)

    def OnClsStat(self, event):
        log = Login(self, -1)
        if log.ShowModal() == wx.ID_OK:
            print('success')

    def OnDetail(self, event):
        reg = Register(self, -1)
        if reg.ShowModal() == wx.ID_OK:
            print('register success')

    def OnApplySign(self, event):
        if not self.isRole('ADMIN'):
            wx.MessageBox('权限需要提升！', 'Error')
        else:
            signs = Config.find(where='code=? and sign=\'Y\'', args='applySign')
            itemId = event.GetId()
            label = self.menu.FindItemById(itemId).GetLabel()
            if signs:
                sign = signs[0]
                if sign.value == 'Y' and label == '开' or sign.value == 'N' and label == '关':
                    pass
                elif label == '开':
                    sign.value = 'Y'
                    sign.update()
                elif label == '关':
                    sign.value = 'N'
                    sign.update()

    def OnMaintain(self, event):
        self.maintain_panel = None
        self.changePanel('view.maintain', 'MaintainPanel', self.maintain_panel)

    def login(self):
        log = Login(self, -1)
        if log.log_user:
            self.user = log.log_user
        else:
            if log.ShowModal() == wx.ID_OK:
                self.user = log.log_user

    def OnAbout(self, event):
        dlg = WFundAbout(self)
        dlg.ShowModal()
        dlg.Destroy()

    def Notify(self):
        t = time.localtime()
        st = time.strftime('%Y年%m月%d日 %H时%M分%S秒', t)
        self.SetStatusText('当前时间：' + st, 2)

    def changePanel(self, module, panel_class, panel=None):
        for item in self.panel_list:
            self.hbox.Hide(item)
        if panel not in self.panel_list:
            model = importlib.import_module(module)
            obj_class_name = getattr(model, panel_class)
            panel = obj_class_name(self, -1)
            self.panel_list.append(panel)
            self.hbox.Add(panel, 1, wx.EXPAND)
        self.hbox.Show(panel)
        self.hbox.Layout()

    def OnCloseWindow(self, event):
        self.timer.Stop()
        self.Destroy()

    def isRole(self, auth):
        return self.user.role == auth




