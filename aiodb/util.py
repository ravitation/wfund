#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import logging

logging.basicConfig(level=logging.INFO)


def log_sql(sql, args=()):
    logging.info('SQL:%s ARGS:%s' % (sql, args))

