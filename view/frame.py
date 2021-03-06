#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv
import time
import locale
import importlib
from utils.menu import Menu
from view.fund.about import WFundAbout
from view.fund.explain import WFundExplain
from view.component.login import Login
from view.component.register import Register
from view.fund.sheet import GenSheet
from view.fund.form import Form
from model.common import Config
from resources.images import ICON, SPLASH_PIC, ADD, ALL_INFO
from utils.img_tran import EmbedImg
from utils import util
from config.constants import APPLY_SIGN

from view.fund.detail import FundDetail
from view.fund.per_stat import PerStatPanel
from view.fund.cls_stat import ClsStatPanel
from view.maintain import MaintainPanel
from view.component.user import UserInfo


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
        self.initToolBar()
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
            ("新增申请\tCtrl+N", "新增申请", self.OnApplyFund, 'N'),
            ("", "", "", ''),
            ("关闭\tCtrl+Q", "关闭", self.OnCloseWindow, 'Q')),
            ),("查看", (
                ("经费详情\tCtrl+D", "经费详情", self.OnDetail, 'D'),
                # ("个人统计\tCtrl+P", "", self.OnPerStat, 'P'),
                ("个人统计", (
                    ("未报销\tCtrl+P", "个人统计-未报销", self.OnPerUnPay, 'O', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                    ("已报销\tCtrl+H", "个人统计-已报销", self.OnPerHadPay, 'H', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                )),
                ("组内统计\tCtrl+G", "组内统计", self.OnClsStat, 'G'),
                ("个人信息\tCtrl+Alt+P", "个人信息", self.OnUserInfo, 'P'),
                ("生成表单\tCtrl+Alt+G", "生成表单", self.OnGenSheet, 'P'),
            )), ('管理', (
                ("添加用户\tCtrl+Alt+A", "添加用户", self.OnAddUser, 'A', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                ("登录其他用户\tCtrl+Alt+U", "登录其他用户", self.OnLogOther, 'U', wx.ACCEL_CTRL | wx.ACCEL_ALT),
                ("申请开关", (
                    ("开\tCtrl+Alt+O", "申请开关-开", self.OnApplySign, 'O', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
                    ("关\tCtrl+Alt+C", "申请开关-关", self.OnApplySign, 'C', wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.ITEM_RADIO),
                )),
                ("维护\tCtrl+Alt+W", "维护", self.OnMaintain, 'W', wx.ACCEL_CTRL | wx.ACCEL_ALT)
            )), ("帮助", (
                ("关于\tCtrl+Shift+A", "关于", self.OnAbout, 'A', wx.ACCEL_CTRL | wx.ACCEL_SHIFT),
                ("说明\tCtrl+E", "说明", self.OnExplain, 'E', wx.ACCEL_CTRL)
            ))]

    def initMenu(self):
        self.menu = Menu(self, self.menuData())
        self.initApplySign()

    def initToolBar(self):
        toolbar = self.CreateToolBar()
        bmp_add = EmbedImg(ADD).GetBitmap()
        add_tool = toolbar.AddTool(-1, "新增申请", bmp_add, "新增申请")
        bmp_all = EmbedImg(ALL_INFO).GetBitmap()
        self.Bind(wx.EVT_TOOL, self.OnApplyFund, add_tool)
        all_tool = toolbar.AddTool(-1, "组内统计", bmp_all, "组内经费情况统计")
        self.Bind(wx.EVT_TOOL, self.OnClsStat, all_tool)
        toolbar.Realize()
        pass

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

    def OnPerUnPay(self, event):
        self.SetStatusText('当前页面：个人统计-未报销', 1)
        self.up_pay = None
        self.changePanel('view.fund.per_stat', 'PerStatPanel', self.up_pay, state=False)

    def OnPerHadPay(self, event):
        self.SetStatusText('当前页面：个人统计-已报销', 1)
        self.had_pay = None
        self.changePanel('view.fund.per_stat', 'PerStatPanel', self.had_pay, state=True)

    def OnClsStat(self, event):
        self.SetStatusText('当前页面：组内统计', 1)
        self.per_cls_panel = None
        self.changePanel('view.fund.cls_stat', 'ClsStatPanel', self.per_cls_panel)

    def OnUserInfo(self, event):
        self.SetStatusText('当前页面：个人信息', 1)
        self.user_info = None
        self.changePanel('view.component.user', 'UserInfo', self.user_info)

    def OnDetail(self, event):
        self.SetStatusText('当前页面：详情', 1)
        self.fund_detail_panel = None
        self.changePanel('view.fund.detail', 'FundDetail', self.fund_detail_panel)

    def OnGenSheet(self, event):
        reg = GenSheet(self, -1, self.user)
        if reg.ShowModal() == wx.ID_OK:
            print('success')

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

    def OnExplain(self, event):
        dlg = WFundExplain(self)
        dlg.ShowModal()
        dlg.Destroy()

    def Notify(self):
        locale.setlocale(locale.LC_ALL, 'en')
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        t = time.localtime()
        st = time.strftime('%Y年%m月%d日 %H时%M分%S秒', t)
        self.SetStatusText('当前时间：' + st, 2)

    def changePanel(self, module, panel_class, panel=None, **kw):
        for item in self.panel_list:
            self.hbox.Hide(item)
        if panel not in self.panel_list:
            model = importlib.import_module(module)
            obj_class_name = getattr(model, panel_class)
            panel = obj_class_name(self, -1, self.user, **kw)
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




