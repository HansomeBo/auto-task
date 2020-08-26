# coding=utf-8
# @Time : 2020/7/16 11:09 上午
# @Author : HansomeBo
# @File : unlock.py
# @Software: PyCharm
import logging
import sys
import os
import pymysql
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def unlock():
    db = pymysql.connect("rm-bp15y8hca789o5hp8.mysql.rds.aliyuncs.com", "sjw_jsb_xub", "5929$xUb0", "task_batch")
    sql = "select loan_code, SUBSTRING_INDEX(protocol_key, '_', -1) as protocol_type, my_key from task_batch.t_protocol_lock_record where status = 1 and TIMESTAMPDIFF(minute, create_dttm, now()) > 20"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    while data:
        url = "http://10.253.124.53:9999/task-batch/lock/unLock?loanCode=" + data[0] + "&protocolType=" + data[
            1] + "&myKey=" + data[2]
        requests.get(url)
        data = cursor.fetchone()
    cursor.execute("update protocol.t_accrual_event set cou = 1 where status = '-1'")
    cursor.close()
    db.close()


if __name__ == '__main__':
    log_path = curPath + '/unlock.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_path,
                        filemode='a')
    logging.info("协议解锁调用开始")
    unlock()
    logging.info("协议解锁调用完成")
