#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import decimal

decimal.getcontext().prec = 6


class Field(object):
    def __init__(self, name, column_type, primary__key, default):
        self.name = name
        self.type = column_type
        self.primary_key = primary__key
        self.default = default

    def __str__(self):
        # 返回 表名字 字段名 和字段类型
        return "<%s , %s , %s>" % (self.__class__.__name__, self.name, self.type)


class IntField(Field):
    def __init__(self, name=None, column_type='int(11)', primary_key=False, default=0):
        super().__init__(name, column_type, primary_key, default)
        self._value = default

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError("int value need")
        self._value = value


class StrField(Field):
    def __init__(self, name=None, column_type='varchar(255)', primary_key=False, default=''):
        super().__init__(name, column_type, primary_key, default)
        self._value = default

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("str value need")
        self._value = value


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'float', primary_key, default)
        self._value = default

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError("float value need")
        self._value = value


class DecimalField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'decimal(19, 6)', primary_key, default)
        self._value = default

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, decimal.Decimal):
            raise ValueError("decimal value need")
        self._value = value


class TextField(Field):
    def __init__(self, name=None, column_type='text', primary_key=False, default=''):
        super().__init__(name, column_type, primary_key, default)
        self._value = default

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("text value need")
        self._value = value


if __name__ == '__main__':
    class Test:
        id = IntField()
        name = StrField()
        score = FloatField()
        dec = DecimalField()

    t = Test()
    t.dec = decimal.Decimal('1')/decimal.Decimal('3')
    print(t.dec)
