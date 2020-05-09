# -*- coding:utf-8 -*-
import json
import os
import re
import requests
from random import randint
from time import sleep
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()



def get_proxy():
    return requests.get("http://127.0.0.1:9910/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:9910/delete/?proxy={}".format(proxy))


class Kuaishou():


    __headersWeb = {
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
        #填上你的cookie
        'Cookie': ''
    }

    __PROFILE_URL = "https://live.kuaishou.com/profile/"
    __DATA_URL = "https://live.kuaishou.com/m_graphql"
    __WORK_URL = "https://v.kuaishou.com/fw/photo/"

    __DATA_PATH = './data/'

    def __headersMobile(self):
        num = randint(1, 300)
        with open('./config/ua_mobile.txt', 'r') as f:
            ua = f.readlines()[num].replace('\n', '')
        headers_mobile = {
            'Host': 'v.kuaishou.com',
            'User-Agent':ua,
            # 'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            #填上你的cookie
            'Cookie': '',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers_mobile

    def __parseVideo(self,videoID):

        proxy = get_proxy().get('proxy')
        url = self.__WORK_URL + videoID
        print('Current Task： %s' %url)
        try:
            req = requests.get(url, headers=self.__headersMobile(),proxies={"http": "http://{}".format(proxy)},timeout=(3,7))
            req.raise_for_status()
            req.close()

            soup = BeautifulSoup(req.text,'lxml')
            noWaterMarkVideo = soup.find(attrs={'id': 'hide-pagedata'}).attrs['data-pagedata']
            pattern = re.compile('\"srcNoMark\":"(.*?)"},', re.S)
            real_url = re.findall(pattern, noWaterMarkVideo)[0]
            print(real_url)

            if not os.path.exists(self.__DATA_PATH):
                os.makedirs(self.__DATA_PATH)


            with open(self.__DATA_PATH + 'data.txt','a+',encoding='utf-8') as f:
                f.write(real_url + '\n')
                f.close()
            # sleep(5)
        except Exception as e:
            num = 5
            while num < 1:
                delete_proxy(proxy)
                print('error: %s' %e)
                self.__parseVideo(videoID)
                sleep(3)
                num -= 1

    def setUid(self,uid):
        self.uid = uid
        self.user()

    def user(self):

        payload1 = {'operationName': "privateFeedsQuery",
                    'query': "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n   privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n     pcursor\n     list {\n       id\n       thumbnailUrl\n       poster\n       workType\n       type\n       useVideoPlayer\n       imgUrls\n       imgSizes\n       magicFace\n       musicName\n       caption\n       location\n       liked\n       onlyFollowerCanComment\n       relativeHeight\n       timestamp\n       width\n       height\n       counts {\n         displayView\n         displayLike\n        displayComment\n         __typename\n       }\n       user {\n         id\n         eid\n         name\n        avatar\n         __typename\n       }\n       expTag\n      __typename\n     }\n     __typename\n  }\n }\n",
                    'variables': {'principalId': str(self.uid), 'pcursor': "", 'count': 512}}

        res = requests.post(self.__DATA_URL, headers=self.__headersWeb, json=payload1)

        # print(res.content)
        works = json.loads(res.content.decode(encoding='utf-8'))['data']['privateFeeds']['list']

        # with open("./" + uid + "2.json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        if works != []:
            if works[0]['id'] is None:
                works.pop(0)


            print('Video Count：%s ' %len(works))
            print(works)
            for work in works:
                type = work['workType']
                if type == 'video':
                    work_id = work['id']
                    sleep(3)
                    self.__parseVideo(work_id)

            print('Parse Successful ^-^ \n')

        else:
            print(works)
            sleep(3)
            self.user()



