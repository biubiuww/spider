# -*- coding:utf-8 -*-
import requests
import os
import time
import threading
from bs4 import BeautifulSoup


class myThred(threading.Thread):
    def __init__(self,url,dir,filename):
        threading.Thread.__init__(self)
        self.ThreadID = filename
        self.url = url
        self.dir = dir
        self.filename = filename

    def run(self):
        downloadPic(self.url,self.dir,self.filename)
def getList(url):
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text,'lxml')
        articlelist = soup.select('#container > main > article > div > a')
        articleurls = [articleurl.get('href') for articleurl in articlelist]
        return articleurls
    except Exception as e:
        print(e)
        return None

def getTitle(url):
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text,'lxml')
        title = soup.select('h1.title')[0].get_text()
        return title
    except Exception as e:
        print(e)
        return None

def getImgurl(url):
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text,'lxml')
        imgurl = soup.select('div.entry')[0].p.img['src']
        return imgurl
    except Exception as e:
        print(e)
        return None

def downloadPic(url,dir,filename):
    req = requests.get(url)
    if req.status_code == 200:
        with open(str(dir) + '/' + str(filename) + '.jpg', 'wb+') as f:
            f.write(req.content)
    else:
        print('链接错误: ' + str(req.status_code))

def getLastpage(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    lastnum = soup.select('#dm-fy > li > a')[-2].get_text()
    return int(lastnum)

def getArticles(url):
    imgurls = []
    lastpage = getLastpage(url)
    pageurls = [str(url) + '?page={}'.format(number) for number in range(1,lastpage)]
    for imgurl in pageurls:
        imgurls.append(imgurl)
    return imgurls

def startUrl(url):
    category = int(input('请输入分类ID： '))
    categoryLast = int(input('请输入分类对应的最后页码： '))
    categoryUrl = [str(url) + 'category-' + str(category) + '_{}.html'.format(num) for num in range(1,int(categoryLast) + 1)]
    return categoryUrl

def main(url):
    imglinks = []
    title = getTitle(url)
    articles = getArticles(url)
    filename = 1
    for imgurl in articles:
        imglink = getImgurl(imgurl)
        imglinks.append(imglink)
        print('获取下载链接ing.......' + str(imglink))
    print('共计取得： ' +str(len(imglinks)) + '张图片链接')
    if os.path.exists(title) == False:
        os.mkdir(title)
        threads = []
        for img in imglinks:
            thread = myThred(img, title, filename)
            thread.start()
            threads.append(thread)
        # downloadPic(imglink, title, filename)
            print('下载完成....' + str(filename))
            filename += 1
        for t in threads:
            t.join()
    else:
        print('文件已存在，跳过下载.....' + str(filename))

url = 'https://www.tuao8.com/'

if __name__ == '__main__':
    try:
        starturls = startUrl(url)
        for starturl in starturls:
            articleurls = getList(starturl)
            for articleurl in articleurls:
                print(articleurl)
                main(articleurl)
                time.sleep(3)
                print('图集下载完成，休眠 3S......')
    except Exception as e:
        print(e)