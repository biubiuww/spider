import requests
import os
import threading
import random, time
from bs4 import BeautifulSoup

host = 'https://hh.flexui.win/'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Referer':host
}

class myThred(threading.Thread):
    def __init__(self,url,dir,filename):
        threading.Thread.__init__(self)
        self.ThreadID = filename
        self.url = url
        self.dir = dir
        self.filename = filename

    def run(self):
        download_pic(self.url,self.dir,self.filename)

def download_pic(url,dir,filename):
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            with open('pic' + '/' + str(dir) + '/' + str(filename), 'wb+') as f:
                f.write(req.content)
                # print('下载完成.......' + str(filename))
        else:
            print("发生错误，跳过下载....." + str(req.status_code))
    except TimeoutError as e:
        print("链接超时: " + str(e))

def open_url(url):
    try:
        req = requests.get(url,headers=headers)
        req.encoding = req.apparent_encoding
        return req
    except (TimeoutError,ConnectionError,requests.exceptions.ConnectionError) as e:
        print('链接超时' + str(e))

def get_page(url):
    url_list = []
    html = open_url(url)
    soup = BeautifulSoup(html.text,'lxml')
    article_url = soup.select('tbody > tr > td.tal > h3 > a')
    for url in article_url:
        url = str(host) + url.get('href')
        url_list.append(url)
    return url_list

def get_article(url):
    img_all =[]
    html = open_url(url)
    soup = BeautifulSoup(html.text,'lxml')
    title = soup.select('td > h4')[0]
    title = title.get_text()
    img_urls = soup.select("input[type='image']")
    for img_url in img_urls:
        img_url = img_url.get('data-src')
        img_all.append(img_url)
    img_sum = len(img_all)
    print('当前帖子：\n' + str(title) + '\n共计取到 ' + str(img_sum) + ' 张图片连接......')
    if os.path.exists(title) == False:
        os.makedirs('pic' + '/' + str(title))
        threads = []
        for imgurl in img_all:
            imgname = imgurl.split('/')[-1]
            thread = myThred(imgurl,title,imgname)
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        timer = random.randint(2,5)
        print('下载完成............\n' + '休眠 ' + str(timer) + ' 秒......')
        time.sleep(timer)
    else:
        print("文件夹已存在，跳过下载。")

if __name__ == '__main__':
    offset = 1
    while offset <= 2:
        page_url = 'https://hh.flexui.win/thread0806.php?fid=16&search=&page=' + str(offset)
        try:
            pagelist = get_page(page_url)
            for url in pagelist:
                if url == 'https://hh.flexui.win/read.php?tid=5877':
                    print("pass")
                elif url == 'https://hh.flexui.win/htm_data/16/1106/524942.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1808/344501.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1110/622028.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1706/2424348.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1707/2519480.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/0805/136474.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1109/594741.html':
                    print('pass')
                elif url == 'https://hh.flexui.win/htm_data/16/1812/3351645.html':
                    print('pass')
                else:
                    get_article(url)
        except Exception as e:
            print('发生错误....跳过下载......' + str(e))
        offset += 1
