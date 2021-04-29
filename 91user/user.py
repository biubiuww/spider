import requests, re
import urllib.parse as up
from time import sleep
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': '__cfduid=dda7b976a0a240beb0968fd6673951c471618894642; CLIPSHARE=jkaaau6k1p151iqhto35fsgrnl; mode=d',
    'Host': '91porn.com',
    'Referer': 'http://91porn.com/uvideos.php?UID=', #fe7dCN6lNv5VirM8tSKWVndvRtHMSVyeHRRNQDEbKvUfjKzE
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}
proxies = {
  'http': 'http://127.0.0.1:1080',
  'https': 'http://127.0.0.1:1080'
}
def get_page(url):
    page = requests.get(url,headers=headers,proxies=proxies)
    page.encoding = page.apparent_encoding
    html = BeautifulSoup(page.text,'lxml')
    if html != None:
        return html
    else:
        return None


class User():

    def __init__(self,uid):
        self.uid = uid
        self.start_url = 'http://91porn.com/uvideos.php?UID={}'.format(self.uid)
        self.num = self.__page_num()

    def __page_num(self):
        page = get_page(self.start_url)
        page_num = page.select('ul.nav.navbar-nav.navbar-right > a')[-1].get_text()
        num = re.findall(r'[0-9]\d',page_num)[0]
        flag = int(num) // 8
        if flag == 0:
            flag = 1
            return flag
        elif flag == 1:
            return flag
        else:
            flag += 2
            return flag


    def __parse_user(self):
        urls = ['http://91porn.com/uvideos.php?UID={}&page={}'.format(str(self.uid),str(num))for num in range(1,int(self.num))]
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
        data_list = []
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
            sleep(1)
            data_list.append(new_data)
        # return new_data
        print(data_list)

