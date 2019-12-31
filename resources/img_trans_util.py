#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import base64


if __name__ == '__main__':
    if __name__ == '__main__':
        with open('../imgs/icon.ico', 'rb') as f:
            data = base64.b64encode(f.read())
            print(data)
