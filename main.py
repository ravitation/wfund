#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx
from wx import adv
from aiodb.pool import init_connection, destory_connection
from view.frame import WFundFrame
from config.config import Db
from config.data import start_on, icon
from config.img import EmbedImg


class App(wx.App):
    def OnInit(self):
        bmp = EmbedImg(start_on).GetBitmap()
        adv.SplashScreen(bmp, adv.SPLASH_CENTER_ON_SCREEN | adv.SPLASH_TIMEOUT, 1000, None, -1)
        wx.Yield()
        self.init_db()
        frame = WFundFrame(None, -1)
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
