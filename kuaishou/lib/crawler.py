# -*- coding:utf-8 -*-
import re,requests
import json
from bs4 import BeautifulSoup
import os
from time import sleep
from random import randint

class Kuaishou(object):

    PROFILE_URL = "https://live.kuaishou.com/profile/"
    DATA_URL = "https://live.kuaishou.com/m_graphql"
    WORK_URL = "https://v.kuaishou.com/fw/photo/"

    DATA_PATH = '../data/'

    requests.packages.urllib3.disable_warnings()

    __headers_web__ = {
        'accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Cookie': 'did=web_0d328ca9a8f40548a70d83fb820e8ce4; didv=1588218275488; clientid=3; client_key=65890b29;'
    }

    def __headersMobile__(self):
        num = randint(1, 300)
        with open('../config/ua_mobile.txt', 'r') as f:
            ua = f.readlines()[num].replace('\n', '')
        headers_mobile = {
            'Host': 'v.kuaishou.com',
            'User-Agent':ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': 'did=web_0d328ca9a8f40548a70d83fb820e8ce4; didv=1588218275488; clientid=3;',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers_mobile

    def __init__(self,uid):
        self.uid = uid

    def __parseVideo__(self):
        url = self.WORK_URL + self.uid
        print('Current Task： %s' %url)
        req = requests.get(url, headers=self.__headersMobile__())

        soup = BeautifulSoup(req.text,'lxml')
        noWaterMarkVideo = soup.find(attrs={'id': 'hide-pagedata'}).attrs['data-pagedata']
        pattern = re.compile('\"srcNoMark\":"(.*?)"},', re.S)
        real_url = re.findall(pattern, noWaterMarkVideo)[0]


        if not os.path.exists(self.DATA_PATH):
            os.makedirs(self.DATA_PATH)


        with open(self.DATA_PATH + 'ks.txt','a+',encoding='utf-8') as f:
            f.write(real_url + '\n')
            f.close()

    def User(self):
        payload = {"operationName": "privateFeedsQuery",
                   "variables": {"principalId": self.uid, "pcursor": "", "count": 999},
                   "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        res = requests.post(self.DATA_URL, headers=self.__headers_web__, json=payload)

        works = json.loads(res.content.decode(encoding='utf-8'))['data']['privateFeeds']['list']

        # with open("./" + uid + "2.json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        if works != None:
            if works[0]['id'] is None:
                works.pop(0)


            print('Video Count：%s ' %len(works))

        for work in works:
            type = work['workType']
            if type == 'video':
                work_id = work['id']
                sleep(3)
                self.__parseVideo__(work_id)

        print('Parse Successful ^-^ \n')





