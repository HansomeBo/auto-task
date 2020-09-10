# coding=utf-8
# @Time : 2020/9/10 9:52 上午
# @Author : HansomeBo
# @File : buy_back.py
# @Software: PyCharm
import sys
import time

from shoujin import shoujin_api, shoujin_db


def buy_back(loan_code):
    # 查询应回购期数
    period = shoujin_db.get_purchase_period(loan_code)
    if period is None:
        print(loan_code + "查不到应回购的期数")
        return
    # 生成回购记录
    flag_buy_back = shoujin_api.generate_puchase(loan_code, 'ZH2016040614245559', period)
    print('生成回购记录 loan_code : ' + loan_code + ',period : ' + str(period) + ',response : ' + flag_buy_back)
    # 休眠两秒后解锁
    time.sleep(2)
    my_key = shoujin_db.get_lock_my_key(loan_code)
    if my_key:
        shoujin_api.unlock(loan_code, 'megre', my_key)


if __name__ == '__main__':
    for loan_code in sys.argv:
        if str(loan_code).find('JKSQ') >= 0:
            buy_back(loan_code)
    shoujin_db.close_db()
