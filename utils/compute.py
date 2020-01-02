#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import decimal


class Compute:
    @classmethod
    def zero(cls):
        return decimal.Decimal('0')

    @classmethod
    def add(cls, a, b):
        return a + b

    @classmethod
    def get(cls, dec):
        return round(dec, 2)

    @classmethod
    def parse(cls, str):
        return decimal.Decimal(str)


if __name__ == '__main__':
    a = decimal.Decimal(1115615.50000) + decimal.Decimal(15.51001)
    print(a)

