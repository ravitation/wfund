#!/usr/bin/env python
# _*_ coding=utf-8 _*_


class Db:
    # host = '127.0.0.1'
    host = '192.168.3.7'
    port = 3306
    # db = 'pytk'
    db = 'wfund'
    user = 'root'
    password = 'root'
    charset = 'utf8'
    maxsize = 10
    minsize = 1
    autocommit = True


mail_template = '''
  <p>
    <b>今报销%s经费申请%s（元）</b>
    <p style="text-indent: 1em;">
      各项费用报销金额如下：<br/>
          <span style="display: block; text-indent: 2em;">餐费：%s（元）</span>
          <span style="display: block; text-indent: 2em;">出租：%s（元）</span>
          <span style="display: block; text-indent: 2em;">油费：%s（元）</span>
          <span style="display: block; text-indent: 2em;">杂项：%s（元）</span>
          <br/>
      <span style='color: #F0C'><b>请确认是否已收到，并回复邮件。</b></span>
    </p>
  </p>
'''


if __name__ == '__main__':
    cont = mail_template % ('cph', '12','12','12','12','12')
    print(cont)
