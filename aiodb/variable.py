#!/usr/bin/env python
# _*_ coding=utf-8 _*_


__pool = None
__loop = None


def __getattr__(name):
    if str(name).endswith('__loop'):
        return __loop
    elif str(name).endswith('__pool'):
        return __pool
