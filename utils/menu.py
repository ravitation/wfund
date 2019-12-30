#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx


class Menu(wx.MenuBar):
    def __init__(self, frame, menu_data):
        wx.MenuBar.__init__(self)
        for eachMenuData in menu_data:
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            self.Append(self.createMenu(menuItems), menuLabel)
            frame.SetMenuBar(self)

    def createMenu(self, menuItems):
        menu = wx.Menu()
        for eachItem in menuItems:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.Append(-1, label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler, key_code, flags=wx.ACCEL_CTRL, kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)
        if key_code:
            acceltbl = wx.AcceleratorTable([(flags, ord(key_code), menuItem.GetId())])
            self.SetAcceleratorTable(acceltbl)
