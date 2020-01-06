#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from aiodb.base import Model
from aiodb.fields import IntField, StrField, FloatField, DecimalField, TextField


class FundApply(Model):
    __table__ = 'tb_fund_apply'
    id = IntField(primary_key=True)
    kind = StrField(column_type='varchar(5)')
    state = StrField(column_type='varchar(5)')
    money = DecimalField()
    date = StrField(column_type='varchar(25)')
    reason = StrField(column_type='varchar(500)')
    persons = StrField(column_type='varchar(500)')
    create_time = StrField(column_type='varchar(25)')
    update_time = StrField(column_type='varchar(25)')
    user_id = IntField()


class FundPayRecord(Model):
    __table__ = 'tb_fund_pay_record'
    id = IntField(primary_key=True)
    money = DecimalField()
    create_time = StrField(column_type='varchar(25)')
    user_id = IntField()


class FundProvide(Model):
    __table__ = 'tb_fund_provide'
    id = IntField(primary_key=True)
    money = DecimalField()
    create_time = StrField(column_type='varchar(25)')
    user_id = IntField()


class FundKind(Model):
    __table__ = 'tb_fund_kind'
    id = IntField(primary_key=True)
    code = StrField(column_type='varchar(10)')
    value = StrField(column_type='varchar(50)')

    @classmethod
    def all(cls):
        return {item.code: item.value for item in FundKind.find()}

    @classmethod
    def all_name(cls):
        return [k.value for k in cls.find()]


def init():
    kinds = [{'code': '01', 'value':  '餐费'},
             {'code': '02', 'value':  '出租'},
             {'code': '03', 'value':  '油费'},
             {'code': '04', 'value':  '杂项'}]

    FundApply.drop()
    FundApply.create()
    FundPayRecord.drop()
    FundPayRecord.create()
    FundProvide.drop()
    FundProvide.create()
    FundKind.drop()
    FundKind.create()

    for item in kinds:
        f = FundKind(**item)
        f.save()


if __name__ == '__main__':
    from aiodb.pool import init_connection, destory_connection
    from config.config import Db

    init_connection(**Db.__dict__)
    init()
    destory_connection()
    pass
