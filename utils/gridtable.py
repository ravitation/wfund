#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.grid


class GridTable(wx.grid.Grid):
    def __init__(self, parent, table=None):
        wx.grid.Grid.__init__(self, parent, -1)
        if table:
            self.SetTable(table, True)

        renderer = wx.grid.GridCellAutoWrapStringRenderer()
        self.SetDefaultRenderer(renderer)

        self.SetDefaultRowSize(26, True)
        self.SetRowLabelSize(36)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER_VERTICAL)
        self.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
