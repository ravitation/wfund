#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from aiodb.fields import *
from aiodb.exec import select, execute
import aiodb.pool as pool
import aiodb.variable as var
import asyncio


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)
        fields = {k: v for k, v in attrs.items() if isinstance(v, Field)}
        table = attrs.get("__table__", None) or name.lower()
        model = attrs.get("__qualname__", None)

        mapping = dict()
        normal = []
        primary_key = None

        for k, v in attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError("Duplicated key for field")
                    primary_key = k
                else:
                    normal.append(k)

        if not primary_key:
            raise RuntimeError("Primary key not found!")

        for k in fields.keys():
            attrs.pop(k)

        normal_fields = list(map(lambda f: '`%s`' % fields.get(f).name if fields.get(f).name is not None else f, normal))

        attrs['__table__'] = table
        attrs['__model__'] = model
        attrs['__fields__'] = fields
        attrs['__normal_fields__'] = normal
        attrs['__primary_key__'] = primary_key
        attrs['__select__'] = 'select `%s`, %s from `%s` ' % (primary_key, ', '.join(normal_fields), table)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s) ' % (table, ', '.join(normal_fields),
                                                                            primary_key, ','.join(
            ['?' for i in range(len(normal_fields) + 1)]))
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?' % (
                table, ', '.join(map(lambda f: '`%s`=?' % (mapping.get(f).name or f), normal_fields)), primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (table, primary_key)

        create_vars = list(map(lambda k: '`%s` %s' % (fields.get(k).name if fields.get(k).name is not None else k, fields.get(k).type), normal))
        attrs['__create__'] = 'CREATE TABLE IF NOT EXISTS `%s` (`%s` %s not null primary key auto_increment, %s);' % (table, primary_key, fields.get(primary_key).type, ', '.join(create_vars))
        attrs['__drop__'] = 'DROP TABLE IF EXISTS `%s`;' % table
        return super().__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, *args, **kw):
        super(Model, self).__init__(**kw)
        # for k, v in kw.items():
        #     setattr(self, k, v)
        # super().__init__()

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(self.__class__.__name__ + ' object have no attributes: %s' % item)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def create(cls):
        n = asyncio.run_coroutine_threadsafe(cls.__create(), var.__loop)
        return n.result()

    @classmethod
    def drop(cls):
        n = asyncio.run_coroutine_threadsafe(cls.__drop(), var.__loop)
        return n.result()

    @classmethod
    def find(cls, where=None, args=None, **kw):
        n = asyncio.run_coroutine_threadsafe(cls.__select(where=where, args=args, **kw), var.__loop)
        return n.result()

    def save(self):
        n = asyncio.run_coroutine_threadsafe(self.__save(), var.__loop)
        return n.result()

    def update(self):
        n = asyncio.run_coroutine_threadsafe(self.__update(), var.__loop)
        return n.result()

    def delete(self, key=None):
        n = asyncio.run_coroutine_threadsafe(self.__delete(key=key), var.__loop)
        return n.result()

    @classmethod
    @asyncio.coroutine
    def __select(cls, where=None, args=None, **kw):
        sql = [cls.__select__]

        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []

        order_by = kw.get('orderBy', None)
        if order_by:
            sql.append('order by')
            sql.append(order_by)

        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value : %s ' % str(limit))

        rs = yield from select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    @asyncio.coroutine
    def __create(cls):
        sql = cls.__create__
        rs = yield from execute(sql, ())
        return rs

    @asyncio.coroutine
    def __save(self):
        args = list(map(self.__get_value, self.__normal_fields__))
        args.append(self.__get_value(self.__primary_key__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            print('failed to insert record: affected rows: %s' % rows)

    @asyncio.coroutine
    def __update(self): 
        args = list(map(self.__get_value, self.__normal_fields__))
        args.append(self.__get_value(self.__primary_key__))
        rows = yield from execute(self.__update__, args)
        if rows != 1:
            print('failed to update record: affected rows: %s' % rows)

    @asyncio.coroutine
    def __delete(self, key=None):
        if key is not None:
            args = [key]
        else:
            args = [self.__get_value(self.__primary_key__)]
        rows = yield from execute(self.__delete__, args)
        if rows != 1:
            print('failed to delete by primary key: affected rows: %s' % rows)

    @classmethod
    @asyncio.coroutine
    def __drop(cls):
        rs = yield from execute(cls.__drop__, ())
        return rs

    def __get_value(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__fields__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                print('using default value for %s : %s ' % (key, str(value)))
                setattr(self, key, value)

        return value


if __name__ == '__main__':
    pool.init_connection()

    class User(Model):
        __table__ = 'tb_user'
        id = IntField(primary_key=True)
        name = StrField()
        age = IntField()
        score = FloatField()

    User.create()
    # u = User(name='name', age=11, score=97.5)
    # print('u create', u)
    # rs = u.save()
    # u.save()
    # print('u save res ', rs)
    users = User.find()
    print('users after save', users)
    u = users[0]
    # u.name = 'zhangsan'
    # print('u update', u)
    # u.update()
    # users = User.find()
    # print('user after update', users)
    u.delete()
    users = User.find()
    print(users)
    User.drop()


