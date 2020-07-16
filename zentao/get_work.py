# coding=utf-8
# @Time : 2020/7/16 9:40 上午
# @Author : HansomeBo
# @File : get_work.py
# @Software: PyCharm
import datetime
import json
import logging
import os

from zentao.work import Work


class GetWork:

    def get_work(self):
        now = datetime.datetime.now()
        week = now.strftime('%w')
        logging.info("获取当前日期 ：" + str(now) + "，星期" + week)
        if int(week) > 5:
            logging.info("当前日期 ：" + str(now) + "，星期" + week + "，不需要进行禅道填写。")
            return None
        abs_path = os.path.dirname(os.path.realpath(__file__))
        work_list_path = abs_path + '/work_map.json'
        work_list = {}
        with open(work_list_path, 'r') as json_file:
            work_list = json.load(json_file)
        # work_str = urlopen(Config.work_json).read().decode("utf-8")
        # work_list = json.loads(work_str)
        date = now.strftime('%Y-%m-%d')
        month = now.strftime('%m')
        work = Work(work_list.get(date), date, month)
        logging.info("转化出来的work对象：" + str(work))
        return work


if __name__ == '__main__':
    print(GetWork.get_work(None))
