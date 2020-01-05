#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from aiodb.pool import init_connection, destory_connection
from web2.htmlframe import HtmlFrame
from config.config import Db
from web.page.index import cont


class App(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = HtmlFrame(None,"Web")
        # frame = MainFrame(None, -1, "Web")
        frame.Center()
        frame.Show()
        self.SetTopWindow(frame)
        return True

    def init_db(self):
        init_connection(**Db.__dict__)

    def OnExit(self):
        destory_connection()
        print("OnExit")
        return -1


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()

