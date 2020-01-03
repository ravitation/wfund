#!/usr/bin/env python
# _*_ coding=utf-8 _*_
from utils.util import max_times


dic = {(0, 0): '曹培贺', (0, 1): '2.50', (0, 2): '2.50', (0, 3): '12.00', (1, 0): 'test', (1, 1): '5.00'}

col = {}

cols = max_times([k[0] for k in dic.keys()])
rows = max_times([k[1] for k in dic.keys()])

print(cols, rows)

if __name__ == '__main__':
    pass
