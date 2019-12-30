#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import asyncio
import logging
import aiomysql
from threading import Thread
import aiodb.variable as var


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def init_loop():
    loop = var.__loop = asyncio.new_event_loop()
    thr = Thread(target=start_loop, args=(loop,))
    thr.setDaemon(True)
    thr.start()



@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info(' start creating database connection pool')
    pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )
    return pool


@asyncio.coroutine
def destroy_pool():
    if var.__pool is not None:
        var.__pool.close()
        yield from var.__pool.wait_closed()


def init_connection(**kw):
    if not var.__loop:
        init_loop()
    n = asyncio.run_coroutine_threadsafe(create_pool(var.__loop, **kw), var.__loop)
    var.__pool = n.result()


def destory_connection():
    if not var.__loop:
        init_loop()
    asyncio.run_coroutine_threadsafe(destroy_pool(), var.__loop)


if __name__ == '__main__':
    class Db:
        host = '127.0.0.1'
        port = 3306
        db = 'pytk'
        user = 'root'
        password = 'root'
        charset = 'utf8'
        maxsize = 10
        minsize = 1
        autocommit = True
    init_connection(**Db.__dict__)
    print(var.__pool)
