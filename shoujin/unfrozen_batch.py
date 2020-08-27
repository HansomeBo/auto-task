# coding=utf-8
# @Time : 2020/8/27 10:32 上午
# @Author : HansomeBo
# @File : unfrozen_batch.py
# @Software: PyCharm
import random
import datetime

import pymysql
import requests


def unfrozen_trade(fund_acc, amt):
    order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000000000, 20000000000))
    print(str(fund_acc) + "," + str(amt) + "," + order_id)
    param_json = '{"typeName":"S000013","businCode":"107","payFundAcc":"' + fund_acc + '","subCode":null,"prdCode":null,"amt":"' + str(
        amt) + '","currType":null,"inCome":null,"vol":null,"targFundAcc":null,"summary":null,"startDate":null,"endDate":null,"assoSerial":null,"investAmt":null,"frozenFlag":null,"strategy":"cmbc","orderId":"' + order_id + '","mode":"0","notifyUrl":null,"notifyMode":null,"returnUrl":null,"usrId":null,"fundAcc":"' + fund_acc + '","priDomain":null,"remark":null,"remark1":null,"remark2":null,"remark3":null,"remark4":null,"remark5":null,"pageChannel":null}';
    response = requests.post('http://10.253.102.157:8416/trade/tradeRequest', param_json,
                             headers={'Content-Type': 'application/json'})
    print(response.text)


if __name__ == '__main__':
    db = pymysql.connect("172.31.20.11", "root", "sjadminos", "dz")
    sql = 'select account_code,diff from account_compare_result_check t where diff > 0 and status = 0'
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    while data:
        unfrozen_trade(data[0], data[1])
        data = cursor.fetchone()
    cursor.close()
    db.close()
