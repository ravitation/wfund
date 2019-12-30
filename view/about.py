#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
import wx.html


class WFundAbout(wx.Dialog):
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
            <b>WFund</b> Is a collection of tools. It is
            based on the wxPython,
        </p>
        <p>
            Copyright &copy; 1997-2006.
        </p>
        </body>
        </html>
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, '关于 WFund', size=(440, 260))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "确认")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

