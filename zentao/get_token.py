# coding=utf-8
# !/usr/bin/env python

import requests
import hashlib
import re

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
    token = GetToken().get_token()
    print(token)
    print(token[1])
    url = "http://10.253.40.224:8018/zentao/my-task.html"
    text = requests.get(Config.host + "/zentao/my-task.html",
                        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                        cookies=token[1]).text
    # print(text)
    str = "<a href='/zentao/task-view-638.html' style='color: '>7月资产端日常任务-徐博</a>"
    s = re.search("(<a href[^\d]+)([\d]+)(\.html)(.*7月.*</a>)", text)
    print(s.group())
    print(s.group(2))
