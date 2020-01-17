#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import smtplib
from model.common import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from utils.decorator import async_fun
from config.constants import MAIL_HOST, MAIL_PORT, MAIL_SENDER, MAIL_PASS


class Email:
    def __init__(self, content, sender, pwd, to, cc=None, subject='', sender_text='', to_text='', atts=[]):
        self.content = content
        if sender:
            self.sender = sender
            self.pwd = pwd
        else:
            self.sender = Config.get_value(MAIL_SENDER)
            self.pwd = Config.get_value(MAIL_PASS)
        if sender_text:
            self.sender_text = sender_text
        else:
            self.sender_text = self.sender
        self.to = to
        self.to_text = to_text
        self.subject = subject
        self.cc = cc
        self.atts = atts
        pass

    def message(self):
        if len(self.atts) == 0:
            message = MIMEText(self.content, 'html', 'utf-8')
            message['From'] = Header(self.sender_text, 'utf-8')
            message['To'] = Header(self.to_text, 'utf-8')
            message['Subject'] = Header(self.subject, 'utf-8')
        else:
            message = MIMEMultipart()
            message['From'] = Header(self.sender_text, 'utf-8')
            message['To'] = Header(self.to_text, 'utf-8')
            message['Subject'] = Header(self.subject, 'utf-8')
            message.attach(MIMEText(self.content, 'plain', 'utf-8'))
            for att in self.atts:
                file = MIMEText(open(att[1], 'rb').read(), 'base64', 'utf-8')
                file["Content-Type"] = 'application/octet-stream'
                file["Content-Disposition"] = 'attachment; filename=' + att[0]
                message.attach(file)
        return message

    @async_fun
    def send(self):
        try:
            smtp_obj = smtplib.SMTP_SSL(Config.get_value(MAIL_HOST), Config.get_value(MAIL_PORT))
            smtp_obj.login(self.sender, self.pwd)
            smtp_obj.sendmail(self.sender, [k for k in ([self.to] + [self.cc]) if k is not None],
                              self.message().as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

