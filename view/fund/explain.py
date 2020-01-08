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
                    <td align="center"><h1>WFund 使用说明</h1></td>
                </tr>
            </table>
        </center>
        <p>
            <h5>菜单说明</h5>
            <dl>
                <dt>操作</dt>
                <dd>新增申请：录入申请</dd>
                <dd>关闭：关闭本应用</dd>
                <dt>查看</dt>
                <dd>经费详情：截止目前经费情况</dd>
                <dd>个人统计-未报销：截止目前个人尚未报销申请</dd>
                <dd>个人统计-已报销：截止目前个人已报销申请</dd>
                <dd>组内统计：截止目前组内尚未报销申请统计</dd>
                <dt>管理（管理员）</dt>
                <dd>添加用户：增加新用户</dd>
                <dd>登录其他用户：用其他用户登录</dd>
                <dd>申请开关-开：选中时可以新增申请</dd>
                <dd>申请开关-关：选中时暂不可新增申请</dd>
                <dd>维护：用户及经费发放</dd>
                <dt>帮助</dt>
                <dd>关于：关于本应用</dd>
                <dd>说明：本应用说明</dd>
            <dl>
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

