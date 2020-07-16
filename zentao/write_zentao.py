# coding=utf-8
# @Time : 2020/7/16 11:09 上午
# @Author : HansomeBo
# @File : write_zentao.py
# @Software: PyCharm

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import logging
import requests

from zentao.config import Config
from zentao.get_token import GetToken
from zentao.get_work import GetWork


class WriteZentao:

    def __init__(self):
        print("__init__")


if __name__ == '__main__':
    log_path = curPath + '/write_zentao.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_path,
                        filemode='w')
    # 获取任务明细
    work = GetWork.get_work(None)
    if work:
        # 登录zentao
        token = GetToken().get_token()
        # 填写禅道
        if token:
            url = Config.host + Config.task_url
            data = 'id[1]=1&dates[1]=' + work.date + '&consumed[1]=8&left[1]=8&work[1]=' + work.work
            logging.info("填写禅道url:" + url + ",data:" + data)
            result = requests.post(url, data=data.encode("utf-8"),
                                   headers={"Content-Type": "application/x-www-form-urlencoded"},
                                   cookies=token[1])
        else:
            logging.info("登录失败")
    else:
        logging.info("获取工作明细失败")
