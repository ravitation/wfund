#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv
import time
import importlib
from utils.menu import Menu
from view.fund.about import WFundAbout
from view.component.login import Login
from view.component.register import Register
from view.fund.form import Form
from model.common import Config
from resources.images import ICON, SPLASH_PIC
from utils.img_tran import EmbedImg
from utils import util
from config.constants import APPLY_SIGN

from view.fund.detail import FundDetail
from view.fund.per_stat import PerStatPanel
from view.fund.cls_stat import ClsStatPanel
from view.maintain import MaintainPanel


class WFundFrame(wx.Frame):
    def __init__(self, parent, pid):
        self.user = None
        self.title = "WFund - Give me Five"
        wx.Frame.__init__(self, parent, pid, self.title, size=(800, 600))
        ico = EmbedImg(ICON).GetIcon()
        self.SetIcon(ico)
        self.filename = ''
        self.wildcard = "WFund files (*.WFund) | *.WFund|All files (* .*) | *.*"
        self.panel_list = []
        self.SetBackgroundColour('White')

        self.initStatusBar()
        self.login()
        self.splash()
        self.initMenu()
        self.createPanel()

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -1, -1])
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.Notify()

    def menuData(self):
        return [("操作", (
            ("新增申请\tCtrl+N", "", self.OnApplyFund, 'N'),
            ("", "", "", ''),
            ("关闭\tCtrl+Q", "", self.OnCloseWindow, 'Q')),
            ),("查看", (
                ("经费详情\tCtrl+D", "", self.OnDetail, 'D'),
                ("个人统计\tCtrl+P", "", self.OnPerStat, 'P'),
                ("组内统计\tCtrl+G", "", self.OnClsStat, 'G'),
            )), ('管理', (
                ("添加用户\tCtrl+Alt+A", "", self.OnAddUser, 'A', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                ("登录其他用户\tCtrl+Alt+U", "", self.OnLogOther, 'U', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                ("申请开关", (
                    ("开\tCtrl+Alt+O", "", self.OnApplySign, 'O', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
                    ("关\tCtrl+Alt+C", "", self.OnApplySign, 'C', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
                )),
                ("维护\tCtrl+Alt+W", "", self.OnMaintain, 'W', wx.ACCEL_CTRL | wx.ACCEL_ALT)
            )), ("帮助", (
                ("&关于\tCtrl+Shift+A", "", self.OnAbout, 'A', wx.ACCEL_CTRL | wx.ACCEL_SHIFT),
                ("&说明\tCtrl+E", "", self.OnAbout, 'E')
            ))]

    def initMenu(self):
        self.menu = Menu(self, self.menuData())
        self.initApplySign()

    def initApplySign(self):
        signs = Config.find(where='code=? and sign=\'Y\'', args='applySign')
        if signs:
            val = signs[0].value
            if val == 'N':
                id = self.menu.FindMenuItem('管理', '关')
                apply_menu = self.menu.FindItemById(id)
                if apply_menu.IsCheckable():
                    apply_menu.Check(True)
            elif val == 'Y':
                id = self.menu.FindMenuItem('管理', '开')
                apply_menu = self.menu.FindItemById(id)
                if apply_menu.IsCheckable():
                    apply_menu.Check(True)

    def createPanel(self):
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hbox)
        # self.OnPerStat(None)
        self.OnDetail(None)

    def OnApplyFund(self, event):
        sign = Config.get_value(APPLY_SIGN)
        if sign:
            self.form = Form(self, -1, user=self.user)
            if self.form.ShowModal() == wx.ID_OK:
                self.flush()
        else:
            wx.MessageBox('暂时不能申请！', '提示')

    def OnPerStat(self, event):
        self.SetStatusText('当前页面：个人统计', 1)
        self.per_stat_panel = None
        self.changePanel('view.fund.per_stat', 'PerStatPanel', self.per_stat_panel)

    def OnClsStat(self, event):
        self.SetStatusText('当前页面：组内统计', 1)
        self.per_cls_panel = None
        self.changePanel('view.fund.cls_stat', 'ClsStatPanel', self.per_cls_panel)

    def OnDetail(self, event):
        self.SetStatusText('当前页面：详情', 1)
        self.fund_detail_panel = None
        self.changePanel('view.fund.detail', 'FundDetail', self.fund_detail_panel)

    def OnAddUser(self, event):
        if not util.isAdmin(self.user):
            wx.MessageBox('权限需要提升！', 'Error')
            return
        reg = Register(self, -1)
        if reg.ShowModal() == wx.ID_OK:
            print('register success')

    def OnLogOther(self, event):
        if not util.isAdmin(self.user):
            wx.MessageBox('权限需要提升！', 'Error')
            return
        log = Login(self, -1)
        if log.ShowModal() == wx.ID_OK:
            self.user = log.log_user
        self.SetStatusText("登录用户："+self.user.name, 0)
        self.flush()

    def OnApplySign(self, event):
        if not util.isAdmin(self.user):
            wx.MessageBox('权限需要提升！', 'Error')
            self.initApplySign()
        else:
            signs = Config.find(where='code=? and sign=\'Y\'', args=APPLY_SIGN)
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
        if not util.isAdmin(self.user):
            wx.MessageBox('权限需要提升！', 'Error')
            return
        self.SetStatusText('当前页面：维护', 1)
        self.maintain_panel = None
        self.changePanel('view.maintain', 'MaintainPanel', self.maintain_panel)

    def login(self):
        log = Login(self, -1)
        if log.log_user:
            self.user = log.log_user
        else:
            if log.ShowModal() == wx.ID_OK:
                self.user = log.log_user
        self.SetStatusText("登录用户："+self.user.name, 0)

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
            panel = obj_class_name(self, -1, self.user)
            self.panel_list.append(panel)
            self.hbox.Add(panel, 1, wx.EXPAND)
        self.hbox.Show(panel)
        self.hbox.Layout()

    def OnCloseWindow(self, event):
        self.timer.Stop()
        self.Destroy()

    def flush(self):
        for panel in self.panel_list:
            panel.refresh(self.user)

    def splash(self):
        bmp = EmbedImg(SPLASH_PIC).GetBitmap()
        adv.SplashScreen(bmp, adv.SPLASH_CENTER_ON_SCREEN | adv.SPLASH_TIMEOUT, 1000, None, -1)
        wx.Yield()




