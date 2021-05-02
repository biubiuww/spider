import requests, re
import random
import urllib.parse as up
from time import sleep
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3

ua = UserAgent()
proxies = {
  'http': 'http://127.0.0.1:1080',
  'https': 'http://127.0.0.1:1080'
}

def random_headers():
    ip = str(random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255)))) + '.' + str(
        random.choice(list(range(255)))) + '.' + str(random.choice(list(range(255))))

    headers = {
        'X-Client-IP': ip,
        'X-Remote-IP': ip,
        'X-Remote-Addr': ip,
        'X-Originating-IP': ip,
        'x-forwarded-for': ip,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        # 'Cookie': '__cfduid=dda7b976a0a240beb0968fd6673951c471618894642; CLIPSHARE=jkaaau6k1p151iqhto35fsgrnl; mode=d',
        'Host': '91porn.com',
        'Referer': 'http://91porn.com/',  # fe7dCN6lNv5VirM8tSKWVndvRtHMSVyeHRRNQDEbKvUfjKzE
        'User-Agent': ua.random
    }
    return headers

def get_page(url):
    page = requests.get(url,headers=random_headers(),proxies=proxies)
    page.encoding = page.apparent_encoding
    html = BeautifulSoup(page.text,'lxml')
    if html != None:
        return html
    else:
        return None


class User:

    def __init__(self,uid):
        self.uid = uid
        self.start_url = 'http://91porn.com/uvideos.php?UID={}'.format(self.uid)
        self.num = self.__page_num()

    def __page_num(self):
        page = get_page(self.start_url)
        page_num = page.select('ul.nav.navbar-nav.navbar-right > a')[-1].get_text()
        print(page_num)
        num = re.findall(r'[0-9]',page_num)[0]
        print(num)
        flag = int(num) // 8
        if flag <= 0:
            flag = 1
            return flag
        else:
            return flag


    def __parse_user(self):
        urls = ['http://91porn.com/uvideos.php?UID={}&page={}'.format(str(self.uid),str(num))for num in range(1,int(self.num+1))]
        # page = get_page(self.start_url)
        for url in urls:
            print(url)
            page = get_page(url)
            video_urls = page.select('div.well.well-sm > a')
            video_ids = page.select('div.thumb-overlay > img')
            video_names = page.select('span.video-title.title-truncate.m-t-5')
            for url,id,name in zip(video_urls,video_ids,video_names):
                data = {
                    'url':url.get('href'),
                    'id':id.get('src').split('/')[-1].strip('.jpg'),
                    'title':name.get_text()
                }
                yield data

    def parse_video(self):
        video_data = []
        for user_data in self.__parse_user():
            page = get_page(user_data['url'])
            m3u8 = page.find(text=re.compile('.*"%.*"'))
            temp =  m3u8.split('"')[-2]
            m3u8_url = up.unquote(temp).split("'")[1]
            new_data = {
                'url': user_data['url'],
                'id': user_data['id'],
                'title': user_data['title'],
                'm3u8': m3u8_url
            }
            video_data.append(new_data)
        # print(video_data)
        up_users = page.select('span.title-yakov > a > span')[0].get_text()
        all_data = {'uid':self.uid,'name':up_users,'data':video_data}
        print(all_data)
        return all_data

class ClientSqlite:

    def __init__(self, dbName="./91user.db"):
        self.conn = sqlite3.connect(dbName)
        self.cur = self.conn.cursor()

    def close_conn(self):
        self.cur.close()
        self.conn.close()

    def create_table(self):
        sql = '''CREATE table users(
                        id int primary key ,
                        uid varchar(255) not null ,
                        name varchar(255) not null ,
                        data text
                    )'''
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print('[ERROR] %s' + e)
            return False

    def fetchall_table(self,sql,limit_flag=True):
        try:
            war_msg = ' The [{}] is empty or equal None!'.format(sql)
            self.cur.execute(sql)
            if limit_flag == True:
                result = self.cur.fetchall()
                return result if len(result) > 0 else war_msg
            else:
                result = self.cur.fetchone()
                return result if len(result) > 0 else war_msg
        except Exception as e:
            print('[SELECT TABLE ERROR]' + e)

    def inset_update_table(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print('[INSERT/UPDATE TABLE ERROR]' + e)
            return False

test_uid = [
    '3637DMj5U2Y7YRyzO9oivHdmcoRn6Cz38oR7yh9jrTonY4AM',
    '787cUGTgFxeUcKp9wAODVVRi35IDVLjNjygNSkyXcSZfdfmZ'
]
if __name__ == '__main__':
    db = ClientSqlite()
    for i in test_uid:
        user = User(i)
        user.parse_video()