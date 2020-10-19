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
    data = shoujin_db.get_compensatory_list()
    for loan_info in data:
        response = shoujin_api.compensatory(str(loan_info[0]), str(loan_info[1]), str(loan_info[2]))
        print(response)
    shoujin_db.close_db()
