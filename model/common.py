#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from aiodb.base import Model
from aiodb.fields import IntField, StrField, FloatField, DecimalField, TextField


class User(Model):
    __table__ = 'tb_user'
    id = IntField(primary_key=True)
    code = StrField(column_type='varchar(50)')
    name = StrField(column_type='varchar(50)')
    password = StrField(column_type='varchar(128)')
    sex = StrField(column_type='varchar(2)')
    birthday = StrField(column_type='varchar(25)')
    mobile = StrField(column_type='varchar(11)')
    email = StrField(column_type='varchar(200)')
    address = StrField(column_type='varchar(200)')
    home = StrField(column_type='varchar(200)')
    avatar = TextField()
    create_time = StrField(column_type='varchar(25)')
    update_time = StrField(column_type='varchar(25)')
    role = StrField(column_type='varchar(10)')

    @classmethod
    def all(cls):
        return {item.id: item.name for item in User.find()}


class Role(Model):
    __table__ = 'tb_role'
    id = IntField(primary_key=True)
    code = StrField(column_type='varchar(10)')
    name = StrField(column_type='varchar(50)')

    @classmethod
    def all(cls):
        return {item.code: item.name for item in Role.find()}

    @classmethod
    def all_name(cls):
        return [item.name for item in Role.find()]


class Config(Model):
    __table__ = 'tb_config'
    id = IntField(primary_key=True)
    code = StrField()
    value = StrField()
    dsc = StrField(column_type='varchar(500)')
    sign = StrField(column_type='varchar(1)')


if __name__ == '__main__':
    from aiodb.pool import init_connection, destory_connection
    from config.config import Db
    init_connection(**Db.__dict__)
    User.create()
    Role.create()
    Config.create()
    destory_connection()
    pass


