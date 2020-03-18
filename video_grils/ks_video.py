import requests
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
import os
UA = UserAgent()

headers = {
    'Connection': 'close',
    'User-Agent':UA.random
}

video_path = './video/'



def get_page(url):
    '''
    :return: response
    '''
    try:
        req = requests.get(url,headers=headers)
        req.raise_for_status()
        req.close()
        req.encoding = 'utf-8'
        return req
    except Exception as code:
        print(code)
        sleep(3)

def download(url):
    video_name = url[-24:]
    if os.path.exists(video_path+video_name) == True:
        print(video_name + ' 视频已存在，跳过')
        pass
    else:
        try:
            req = requests.get(url,headers=headers)
            req.raise_for_status()
            req.close()
            with open(video_path + video_name,'wb') as f:
                f.write(req.content)
                f.close()
            print(str(video_name) + ' ~下载完成！')
        except Exception as code:
            print(code)
            return None


def parse_xiacoo(html):
    # http://v.xiacoo.com
    soup = BeautifulSoup(html.text, 'lxml')
    video_src = soup.select('source')[0]
    video_url = video_src.get('src').split('?', 1)
    url = video_url[0]
    return url

def parse_xjj(html):
    # https://xjj.show/ks.php
    soup = BeautifulSoup(html.text, 'lxml')
    video_src = soup.find_all('video')[0]
    video_url = video_src.get('src').split('?', 1)
    url = video_url[0]
    return url




if __name__ == '__main__':
    print('1: v.xiacoo.com; 2: xjj.show;')
    select = int(input('Please input your select:'))
    if select == 1:
        start_url = 'http://v.xiacoo.com'
        print('start url: ' + str(start_url))
    elif select == 2:
        start_url = 'https://xjj.show/ks.php'
        print('start url: ' + str(start_url))
    else:
        print('ERROR: check your input!')
        exit()
    while True:
        try:
            video_page = get_page(start_url)
            if video_page == None:
                print('url is None!')
                video_page = get_page(start_url)
            else:
                video_url = parse_xjj(video_page)
                download(video_url)
            sleep(randint(1,3))
        except TimeoutError as code:
            print(code)