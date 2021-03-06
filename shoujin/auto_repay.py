# coding=utf-8
# @Time : 2020/10/19 4:45 下午
# @Author : HansomeBo
# @File : compensatory.py
# @Software: PyCharm
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from shoujin import shoujin_db, shoujin_api

if __name__ == '__main__':
    faxi_data = shoujin_db.get_faxireduce_list()
    for loan_info in faxi_data:
        response = shoujin_api.faxi_reduce(str(loan_info[0]), str(loan_info[1]))
        print(response)

    xinyongfei_data = shoujin_db.get_xinyongfei_list()
    for loan_info in xinyongfei_data:
        response = shoujin_api.repay_compensatory(str(loan_info[0]), str(loan_info[1]), str(loan_info[2]))
        print(response)
        if response.find("用户余额不足") != -1:
            print("信用飞余额不足，退出")
            break

    kuainiu_data = shoujin_db.get_kuainiu_list()
    for loan_info in kuainiu_data:
        response = shoujin_api.repay_compensatory(str(loan_info[0]), str(loan_info[1]), str(loan_info[2]))
        print(response)
        if response.find("用户余额不足") != -1:
            print("快牛余额不足，退出")
            break


    # buy_back_list = shoujin_db.get_buy_back_list()
    # for loan_info in buy_back_list:
    #     response = shoujin_api.repay_puchase(str(loan_info[0]), str(loan_info[1]))
    #     print(response)
    # shoujin_db.update_outer_transaction()
    shoujin_db.close_db()
