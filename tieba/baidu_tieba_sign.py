# -*- coding:utf-8 -*-
import logging
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
import urllib.error
import re

if __name__ == '__main__':
    log_path = curPath + '/baidu_tieba_sign.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_path,
                        filemode='a')
    head = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-cn',
        'Connection': 'keep-alive',
        'Cookie': 'st_data=045030c86caf5f8ca06f27a74b2dfb412eade24f9afb121d764953efa2e048de5cd955ae6383c7a6349eb1999860ab9b69737a010ae9ff7fb5429972ce20c80c750393ddc5ee80e0e16aba1995c2d6fdf97c42ea28705b6d1bc69b76567dcb57fc6585ff575057340b80ee003c731ec871f284c7818f0106ae20487c5bdcd6c9; st_key_id=17; st_sign=036b77e4; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1594968474; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1594190783,1594791616,1594889596,1594966521; 1749587064_FRSVideoUploadTip=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; wise_device=0; H_PS_PSSID=1466_32231_32295; BAIDUID=CCAC021A9F117A749274201EFD0C42E2:FG=1; showCardBeforeSign=1; rpln_guide=1; bdshare_firstime=1594791616076; STOKEN=8b31cceae68e3601914859e070aeecd74444a4429a8908de969d1b5957477a3c; MCITY=-131%3A; BDUSS=EdXM0ZvUDVzUzdKN2VNZTQ4MldQT3hHbGFTaGxzeFlrZVFnaGhtYXZsWnBTYTFlRVFBQUFBJCQAAAAAAAAAAAEAAAB4lEho3~ff921pYW9taWFvODIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGm8hV5pvIVeU; H_WISE_SIDS=142113_114551_141694_142206_142506_135846_141003_142080_142061_141122_142019_141837_141746_143162_140853_142510_138878_139175_142919_142780_142286_136862_140174_131247_137743_138165_138883_133847_141941_127969_142873_140066_142907_140593_134046_143056_141808_139549_138425_143276_141930_131423_142168_138595_140974_138661_141103_110085; TIEBAUID=72034c46da4e66b03ae117f2; TIEBA_USERTYPE=99184f06e2f12ca8222b63bb; BIDUPSID=748CBF2CE0079F042638CBECA966ED4C; PSTM=1577100738',
        'Host': 'tieba.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://tieba.baidu.com/i/i/forum',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    }

    like_url = 'http://tieba.baidu.com/f/like/mylike?v=1547424142305'
    sign_url = 'http://tieba.baidu.com/sign/add'
    tbs = '4fb45fea4498360d1547435295'

    like_result = []
    try:
        html = requests.Session().get(like_url, headers=head).text
        # like_result += re.compile(r'href="/f\?kw=([^ ]+)"').findall(html)
        like_result += re.compile(r'title="([^"]+)">[^<]+</a></td><td>').findall(html)
        logging.info("贴吧签到集合:" + str(like_result))
    except urllib.error.HTTPError as e:
        print(e.reason)

    for name in like_result:
        data = {
            'ie': 'utf-8',
            'kw': name,
            'tbs': tbs
        }
        try:
            logging.info("进行贴吧：" + name + " 签到")
            r = requests.post(sign_url, data=data, headers=head)
            logging.info("贴吧：" + name + " 签到结果：" + str(r))
        except urllib.error.HTTPError as e:
            print(e.reason)
