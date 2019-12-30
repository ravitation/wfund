#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from aiodb.util import log_sql
import asyncio
import aiomysql
import aiodb.variable as var


@asyncio.coroutine
def select(sql, args, size=None):
    log_sql(sql, args)
    with (yield from var.__pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args)
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
    return rs


@asyncio.coroutine
def execute(sql, args, autocommit=True):
    log_sql(sql, args)
    with (yield from var.__pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            yield from conn.commit()
            affected_line = cur.rowcount
            yield from cur.close()
            print('execute : ', affected_line)
        except BaseException as e:
            raise e
        return affected_line

