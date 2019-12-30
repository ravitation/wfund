#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import wx


class NotEmptyValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return NotEmptyValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            wx.MessageBox('the field must contain some text', 'Error')
            textCtrl.SetBackgroundColour('Pink')
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True
        pass

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

