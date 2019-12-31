#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx


class Part:
    @classmethod
    def GenStaticBoxSizer(cls, parent, box_label, items, flags=wx.ALL):
        box = wx.StaticBox(parent, -1, box_label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
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
