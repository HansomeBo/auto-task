# coding=utf-8
# @Time : 2020/8/27 10:32 上午
# @Author : HansomeBo
# @File : unfrozen_batch.py
# @Software: PyCharm
import os
import sys

import pymysql

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from shoujin import shoujin_api

if __name__ == '__main__':
    db = pymysql.connect("172.31.20.11", "root", "sjadminos", "dz")
    sql = 'select account_code,diff from account_compare_result_check t where diff > 0'
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    while data:
        shoujin_api.unfrozen_trade(data[0], data[1], '')
        data = cursor.fetchone()
    cursor.close()
    db.close()
