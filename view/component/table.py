#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid


data = {(1,1): 'Here',
        (2,2):'is',
        (3,3):'some',
        (4,4):'data'
        }


class GenericTable(wx.grid.GridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.GridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels

        self.odd = wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour('sky blue')
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour('sea blue')
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]

    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]

    def IsEmptyCell(self, row, col):
        return self.data.get(row, col) is not None

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        pass

    def GetAttr(self, row, col, kind):
        attr = [self.even]
