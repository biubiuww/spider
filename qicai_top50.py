# -*- coding:utf-8 -*-
# date: 2018年10月15日

import requests
from bs4 import BeautifulSoup
import urllib.request
import re
from  multiprocessing import Pool
import random, time

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host': 'www.qcenglish.com',
    'Referer': 'http://www.qcenglish.com/'
}

url = 'http://www.qcenglish.com'
host = 'http://www.qcenglish.com'

download_path = './'

def get_article(url):
    req = requests.get(url,headers=headers)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text,'lxml')
    try:
        pdf_title = soup.select('#details > dl > dd')[0].get_text()
        download_link = soup.select('#download > li > a')[-1].get('href')
        print('书名：' + pdf_title)
        print('下载链接：' + host + download_link)
        download_url = host + download_link
        download(download_url,pdf_title)
    except IndexError as e:
        print(e)
        pass

def download(url, title):
    file_path = download_path + title + '.zip'
    urllib.request.urlretrieve(url, file_path)
    print('下载完成.......\n')
    print('延迟等待....Hold on!')
    time.sleep(random(3,10))


def get_list(url):
    top_list = []
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text,'lxml')
    pdf_list = soup.select('#rectop2 > ul > li > a')
    for p_list in pdf_list:
        p_list = p_list.get('href')
        top_list.append(p_list)
    # print(top_list)
    p = re.compile('_')
    clear_list = [x for x in top_list if not p.findall(x)]
    return clear_list


if __name__ == '__main__':
    p = Pool()
    top_list = get_list(url)
    for article_url in top_list:
        start_url = host + article_url
        # get_article(start_url)
        start = p.apply_async(get_article(start_url))
    p.close()
    p.join()
    if start.successful():
        print('Top50 下载完成！\n')