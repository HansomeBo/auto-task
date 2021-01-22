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

def get_xinyongfei_list():
    sql = "select distinct t.loan_code, t.period, t.account_no, t.expire_date  from protocol.t_external_organ_repay t           inner join protocol.t_asset_core c on c.loan_code = t.loan_code  where c.product_name like '%XYF%'    and t.expire_date <= current_date    and t.item_type = 'interest'    and t.status = 0    and t.must_amt > 0    and t.account_no = 'ZH20190604151818198629'    and t.loan_code in (select loan_code                        from protocol.t_external_debt h                        where h.status = 0                          and h.expire_date = current_date                          and h.credito_type = 'invest')  order by t.expire_date asc"
    cursor.execute(sql)
    return cursor.fetchall()

def get_kuainiu_list():
    sql = "select distinct t.loan_code, t.period, t.account_no from protocol.t_external_organ_repay t          inner join protocol.t_asset_core c on c.loan_code = t.loan_code where c.product_code = 'PC20200420141427001'   and t.expire_date <= current_date   and t.item_type = 'interest'   and t.status = 0   and t.must_amt > 0   and t.account_no = 'ZH20200417115742830950'   and t.loan_code in (select loan_code from protocol.t_external_debt h where h.status = 0 and h.expire_date = current_date and h.credito_type = 'invest') order by t.expire_date asc"
    cursor.execute(sql)
    return cursor.fetchall()

def get_faxireduce_list():
    sql = "select t.loan_code, t.period from protocol.t_external_organ_fee_asset t  where t.account_no in ('ZH20200417115742830950','ZH20190604151818198629') and date_format(expire_date,'%d') = date_format(current_date,'%d')  and t.status = 0 and t.must_amt > 0"
    cursor.execute(sql)
    return cursor.fetchall()

def get_buy_back_list():
    sql = "select i.loan_code, account_no from protocol.t_external_organ_repay i where 1 = 1 and status = 0 and pay_way = 'repo' and create_datetime > current_date and i.account_no in ('ZH20190604151818198629') group by loan_code,account_no"
    cursor.execute(sql)
    return cursor.fetchall()

def update_outer_transaction():
    db_lmh = pymysql.connect("rm-bp15y8hca789o5hp8.mysql.rds.aliyuncs.com", "sjw_jsb_limh", "jsb_limh", "asset_trans_outer")
    cursor_lmh = db_lmh.cursor()
    sql1 = "update asset_trans_outer.t_external_trade_event a set a.cou = 0 where a.status != 'S' and a.status !='C' and TIMESTAMPDIFF(minute,a.create_dttm,now()) > 40"
    sql2 = "update asset_trans_outer.t_repay_event a set a.cou = 0 where a.status != 2  and status != 3  and TIMESTAMPDIFF(minute,a.create_dttm,now()) > 40"
    cursor_lmh.execute(sql1)
    cursor_lmh.execute(sql2)
    cursor_lmh.close()
    db_lmh.commit()
    db_lmh.close()

if __name__ == '__main__':
    update_outer_transaction()
