#!/usr/bin/python3
# _*_ coding=utf-8 _*_
# @Time    : 2019/5/23 下午10:01
# @Author  : ehoac
# @Email   : ehoac@sina.com
# @File    : decorator.py
# @Software: PyCharm
import wrapt
from threading import Thread


def async_fun(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
