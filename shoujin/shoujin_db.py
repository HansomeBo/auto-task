# coding=utf-8
# @Time : 2020/9/10 2:27 下午
# @Author : HansomeBo
# @File : shoujin_db.py
# @Software: PyCharm
import pymysql

db = pymysql.connect("rm-bp15y8hca789o5hp8.mysql.rds.aliyuncs.com", "sjw_jsb_xub", "5929$xUb0", "task_batch")
cursor = db.cursor()


def close_db():
    cursor.close()
    db.close()


def get_purchase_period(loan_code):
    period_sql = "select min(period) from protocol.t_interior_debt where status = '0' and credito_type = 'invest' and loan_code = %s"
    cursor.execute(period_sql, loan_code)
    return cursor.fetchone()[0]


def get_lock_my_key(loan_code):
    unlock_sql = "select my_key from task_batch.t_protocol_lock_record where loan_code = %s and status = '1'"
    cursor.execute(unlock_sql, loan_code)
    return cursor.fetchone()[0]
