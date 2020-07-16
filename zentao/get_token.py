#!/usr/bin/env python

import requests
import hashlib
import re
import datetime

from zentao.config import Config


class GetToken():

    def get_token(self):
        loginUrl = Config.host + "/zentao/user-login.html"
        headers_1 = {"Content-Type": "application/x-www-form-urlencoded"}  # 定义headers

        get_sid = requests.get(loginUrl)  # get方法请求登录页面，用于获取SID
        get_sid.encoding = 'utf-8'
        verifyRand = re.findall("id='verifyRand' value='(\d+)'", get_sid.text)[0]  # 获取verifyRand值
        SID = get_sid.cookies["zentaosid"]
        # print(SID)

        hlFirst = hashlib.md5()
        hlFirst.update(Config.pwd.encode(encoding='utf-8'))  # 第一次对密码进行加密
        # print('Md5 第一次加密结果 = ' + hlFirst.hexdigest())
        passwordResult = hlFirst.hexdigest() + verifyRand
        # print("passwordResult=" + passwordResult)
        hlLast = hashlib.md5()
        hlLast.update(passwordResult.encode(encoding='utf-8'))  # 第二次加密
        # print('Md5 第二次加密结果 = ' + hlLast.hexdigest())

        # 定义请求参数body
        bodyRequest = {"account": Config.username, "password": hlLast.hexdigest(), "passwordStrength": 1,
                       "referer": "/zentao/", "verifyRand": verifyRand, "keepLogin": 1}

        # 定义cookies
        loginCookies = dict(zentaosid=SID, lang='zh-cn', keepLogin='on')
        loginRequest = requests.post(loginUrl, data=bodyRequest, cookies=loginCookies)

        token = loginRequest.cookies['zp']  # 从cookies中获取token

        # 测试一下：访问我的地盘页面
        test = requests.get(Config.host + "/zentao/my/", cookies=loginRequest.cookies)

        return token, loginRequest.cookies


if __name__ == '__main__':
    host = "http://10.253.40.224:8018"
    url = host + "/zentao/task-recordEstimate-638.html?onlybody=yes"
    cookies = GetToken().get_token()[1]
    text_1 = requests.get(url, cookies=GetToken().get_token()[1]).text
    headers_1 = {"Content-Type": "application/x-www-form-urlencoded"}
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    work = "百行征信漏报数据的补报ssss"
    data = 'id[1]=1&dates[1]=' + date + '&consumed[1]=8&left[1]=8&work[1]=' + work
    result = requests.post(url, data=data.encode("utf-8"), headers=headers_1, cookies=GetToken().get_token()[1])
    print(result.text)
