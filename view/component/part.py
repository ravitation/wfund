#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid
from view.component.table import GenericTable
from utils.gridtable import GridTable


class Part:
    @classmethod
    def GenStaticBoxSizer(cls, parent, box_label, items, flags=wx.ALL, static_flags=wx.VERTICAL):
        box = wx.StaticBox(parent, -1, box_label)
        sizer = wx.StaticBoxSizer(box, static_flags)
        for item in items:
            sizer.Add(item, 0, flags, 5)
        return sizer

    @classmethod
    def GenShowText(cls, parent, txt, font=None, style=wx.NORMAL):
        text = wx.StaticText(parent, -1, str(txt), style=style)
        print(txt, text)
        if font:
            text.SetFont(font)
        return text
    pass

    @classmethod
    def GenGrid(cls, parent, colLabels, data):
        table = GenericTable(data=data, colLabels=colLabels)
        grid = GridTable(parent, table)
        grid.SetColSize(0, 180)
        # grid.SetTable(table, True)
        # grid.SetDefaultRowSize(26)
        # grid.SetRowLabelSize(36)
        return grid

    @classmethod
    def CreateMenu(cls, parent,  menuItems):
        menu = wx.Menu()
        for eachItem in menuItems:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = cls.CreateMenu(parent, eachItem[1])
                menu.Append(-1, label, subMenu)
            else:
                cls.createMenuItem(parent, menu, *eachItem)
        return menu

    @classmethod
    def createMenuItem(cls, parent, menu, label, status, handler, key_code, flags=wx.ACCEL_CTRL, kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        parent.Bind(wx.EVT_MENU, handler, menuItem)
        if key_code:
            acceltbl = wx.AcceleratorTable([(flags, ord(key_code), menuItem.GetId())])
            parent.SetAcceleratorTable(acceltbl)

    @classmethod
    def createHorBtn(cls):
        pass
