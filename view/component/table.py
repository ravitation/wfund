#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid
from utils.util import max_times


table_data = {(1,1): 'Here',
        (2,2):'is',
        (3,3):'some',
        (4,4):'data'
        }


class GenericTable(wx.grid.GridTableBase):
    def __init__(self, data=None, rowLabels=None, colLabels=None):
        wx.grid.GridTableBase.__init__(self)
        if data:
            self.data = data
        else:
            self.data = table_data
        self.rowLabels = rowLabels
        self.colLabels = colLabels

        self.odd = wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour('light blue')
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour('sea blue')
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.add = wx.grid.GridCellAttr()
        self.add.SetBackgroundColour('light blue')
        self.add.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.mius = wx.grid.GridCellAttr()
        self.mius.SetBackgroundColour('medium goldenrod')
        self.mius.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    def GetNumberRows(self):
        return max_times([k[1] for k in self.data.keys()])

    def GetNumberCols(self):
        # num = max_times([k[0] for k in self.data.keys()])
        # return num if num >= len(self.colLabels) else len(self.colLabels)
        return len(self.colLabels)

    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
        else:
            return str(col + 1)

    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        else:
            return str(row + 1)

    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None

    def GetValue(self, row, col):
        value = self.data.get((row, col))
        if value is not None:
            return value
        else:
            return ''

    def GetDataValue(self, row, col):
        value = self.data.get((row, col))
        if value is not None:
            return value
        else:
            return ''

    def SetValue(self, row, col, value):
        self.data[(row, col)] = value

    def GetAttr(self, row, col, kind):
        val = self.data.get((row, 1))
        if val != '增加' and val != '报销':
            attr = [self.even, self.odd][row % 2]
        else:
            if self.data.get((row, 1)) == '增加':
                attr = self.add
            else:
                attr = self.mius
        attr.IncRef()
        return attr

    def AppendRows(self, numRows=1):
        # return (self.GetRowsCount() + numRows) <= 50
        return True

    def AppendCols(self, numCols=1):
        return True
