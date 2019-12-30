#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from base64 import b64decode
from io import BytesIO


class EmbedImg(object):
    def __init__(self, data, isBase64=True):
        self.data = data
        self.isBase64 = isBase64

    def GetBitmap(self):
        return wx.Bitmap(self.GetImage())

    def GetData(self):
        data = self.data
        if self.isBase64:
            data = b64decode(self.data)
        return data

    def GetIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        stream = BytesIO(self.GetData())
        return wx.Image(stream)
