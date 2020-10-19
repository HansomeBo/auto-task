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

def get_compensatory_list():
    sql = "select i.loan_code, i.period, r.account_no from protocol.t_interior_debt i          left join protocol.t_asset_core c on c.loan_code = i.loan_code    left join protocol.t_external_organ_repay r on r.loan_code = i.loan_code and r.period = i.period where i.item_type = 'interest'   and r.item_type = 'interest'   and i.expire_date = current_date   and i.status = 0   and r.pay_way = 'commuting'   and i.credito_type = 'invest'   and ((r.account_no = 'ZH20190604151818198629' and         c.product_code in ('PC20190611172657001', 'PC20200319153425002', 'PC20200709132533006')) or        (r.account_no = 'ZH20180228172509002807' and         c.product_code in ('SJ441010', 'SJ441011', 'SJ441012', 'PC20190304104203001', 'PC20190329195814002')) or        (r.account_no = 'ZH20190426154721' and c.product_code in ('PC20190513111412001')) or        (r.account_no = 'ZH20180816140754000862' and         c.product_code in ('PC20190916101027002', 'PC20190916100950001', 'PC20190916101232006')) or        (r.account_no = 'ZH20180306100738000152' and c.product_code in ('SJ439008', 'SJ439006', 'SJ439005')) or        (r.account_no = 'ZH20200417115742830950' and c.product_code in ('PC20200420141427001'))     ) "
    cursor.execute(sql)
    return cursor.fetchall()