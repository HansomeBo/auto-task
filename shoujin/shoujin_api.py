# coding=utf-8
# @Time : 2020/9/10 11:08 上午
# @Author : HansomeBo
# @File : shoujin_api.py
# @Software: PyCharm
import datetime
import random

import requests

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


def unlock(loan_code, protocol_type, my_key):
    url_unlock = "http://10.253.124.53:9999/task-batch/lock/unLock?loanCode=" + loan_code + "&protocolType=" + protocol_type + "&myKey=" + my_key
    print(url_unlock)
    response = requests.get(url_unlock)
    if response.text == 'true':
        return True
    return False


def generate_puchase(loan_code, account_no, period):
    url_buy_back = "http://10.253.124.53:9999/task-batch/test/testPurchase?loanCode=" + loan_code + "&accountNo=" + account_no + "&period=" + str(
        period)
    response = requests.get(url_buy_back)
    if not response.ok:
        return False
    return True

def faxi_reduce(loan_code, period):
    url_buy_back = "/protocol-web/feeRelief/feeReliefByLoanCode?loanCode=" + loan_code + "&period=" + str(period)
    response = requests.get(url_buy_back)
    if not response.ok:
        return False
    return True


def repay_compensatory(loan_code, period, account_no):
    url_compensatory = "http://10.253.124.53:9999/repayment-asset-order-web/repayment/order/repayTrans"
    data = '{"accountNo": "' + account_no + '","channelNo": "auto","loanCode": "' + loan_code + '","repayWay": "3","repayType": "2","period": ' + period + ',"endPeriod": ' + period + '}'
    response = requests.post(url_compensatory, data=data, headers=headers)
    if not response.ok:
        return False
    return response.text


def repay_puchase(loan_code, account_no):
    url_compensatory = "http://10.253.124.53:9999/repayment-asset-order-web/repayment/order/repayTrans"
    data = '{"accountNo": "' + account_no + '","channelNo": "auto","loanCode": "' + loan_code + '","repayWay": "3","repayType": "4"}'
    response = requests.post(url_compensatory, data=data, headers=headers)
    if not response.ok:
        return False
    return response.text


def unfrozen_trade(fund_acc, amt, assoSerial):
    order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000000000, 20000000000))
    print(str(fund_acc) + "," + str(amt) + "," + order_id)
    param_json = '{"typeName":"S000013","businCode":"107","payFundAcc":"' + fund_acc + '","subCode":null,"prdCode":null,"amt":"' + str(
        amt) + '","currType":null,"inCome":null,"vol":null,"targFundAcc":null,"summary":null,"startDate":null,"endDate":null,"assoSerial":"' + assoSerial + '","investAmt":null,"frozenFlag":null,"strategy":"cmbc","orderId":"' + order_id + '","mode":"0","notifyUrl":null,"notifyMode":null,"returnUrl":null,"usrId":null,"fundAcc":"' + fund_acc + '","priDomain":null,"remark":null,"remark1":null,"remark2":null,"remark3":null,"remark4":null,"remark5":null,"pageChannel":null}';
    response = requests.post('http://10.253.102.157:8416/trade/tradeRequest', param_json,
                             headers={'Content-Type': 'application/json'})
    print(response.text)


if __name__ == '__main__':
    print(generate_puchase("JKSQ20200616001169DK", "ZH2016072911360170", 5))
    # print(generate_puchase("JKSQ20200615000350DK", "ZH2016072911360170", 5))
    # print(generate_puchase("JKSQ20200615000350DK", "ZH2016072911360170", 5))
