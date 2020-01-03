#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from aiodb.pool import init_connection, destory_connection
from view.frame import WFundFrame
from config.config import Db


class App(wx.App):
    def OnInit(self):
        self.init_db()
        frame = WFundFrame(None, -1)
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
