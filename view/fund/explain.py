#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html
from view.component.html import HtmlShow


class WFundExplain(wx.Dialog):
    text = '''
        <html>
        <body bgcolor="#ACAA60">
        <center>
            <table bgcolor="#455481" width="100%" cellspacing="0"
                cellpadding="0" border="1">
                <tr>
                    <td align="center"><h1>WFund</h1></td>
                </tr>
            </table>
        </center>
        <p>
            <b>WFund</b>是用于开发五组内部经费记录的工具，以方便组内经费统计<br/>报销。</p>
            <a href='http://www.baidu.com' name='baidu' target='_blank'>Baidu.com</a>
        <p>
            <center>
                Copyright &copy; 2020.
            </center>
        </p>
        </body>
        </html>
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, '关于 WFund', size=(440, 260))
        html = HtmlShow(self, -1, self.text)
        button = wx.Button(self, wx.ID_OK, "确认")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

