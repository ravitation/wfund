#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from model.fund import init as fund_init
from model.common import init as common_init
from config.config import Db
from aiodb.pool import init_connection, destory_connection


def fund_kind_data():
    pass


def main():
    init_connection(**Db.__dict__)
    fund_init()
    common_init()
    destory_connection()


if __name__ == '__main__':
    main()
    pass

