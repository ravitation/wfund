#!/usr/bin/env python
# _*_ coding=utf-8 _*_


class Db:
    host = '127.0.0.1'
    # host = '192.168.3.7'
    port = 3306
    # db = 'pytk'
    db = 'wfund'
    user = 'root'
    password = 'root'
    charset = 'utf8'
    maxsize = 10
    minsize = 1
    autocommit = True


if __name__ == '__main__':
    print(Db.__dict__)
