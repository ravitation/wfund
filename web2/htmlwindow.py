#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx.html2 import WebView


class HtmlWindow(WebView):
    def __init__(self, parent, ID):
        WebView.__init__(self, parent, ID)
