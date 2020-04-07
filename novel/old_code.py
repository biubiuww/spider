import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
from multiprocessing import Pool
from fake_useragent import UserAgent
import time
from random import randint




client = MongoClient()
db = client.novelDB
books = db['t1novel']

'''
book表

book_id
book_name    ---- 书名
author       ---- 作者
book_pic     ---- 略缩图
score        ---- 评分
book_desc    ---- 简介

sort         ---- 分类
process      ---- 状态

1、书名前100页，取id、书名、作者、评分、简介、略缩图 -

2、
'''




def getPage(url):
    UA = UserAgent()
    headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': UA.random
    }

    flag = 0
    req = None
    while flag < 3 or req != None:
        try:
            req = requests.get(url,headers=headers)
            req.raise_for_status()
            req.close()
            req.encoding = req.apparent_encoding
            return req.text
        except:
            flag += 1
            print('重试: %s' % flag)
            time.sleep(3)
            if flag == 3:
                return None

def parsePage(req):
    page = BeautifulSoup(req,'lxml')
    items = page.select('div.hot_sale')
    bookinfo = []
    for item in items:
        data = {
            'book_id':item.select('div.bookinfo > a')[0].get('href'),
            'book_pic':item.select('div.bookimg > a > img')[0].get('data-original'),
            'book_name':item.select('div.detail > p.title')[0].get_text(),
            'author': item.select('p.author')[0].get_text().strip('作者：'),
            'score': item.select('div.score')[0].get_text(),
            'book_desc':item.select('p.review')[0].get_text().split('简介：')[1].strip()
        }
        bookinfo.append(data)
        # yield data
    return bookinfo
    # saveDB(bookinfo)

def saveDB(items):
    for item in items:
        if books.update_one({'book_id':item['book_id'],'book_pic':item['book_pic'],'book_name':item['book_name'],'author':item['author'],'score':item['score'],'book_desc':item['book_desc']},
                            {'$set':item},upsert=True):
            print(item['book_name'])
        else:
            print('save error!')
    # books.insert_many(items)
    # books.update_many(items,upsert=True)
    books.close

def endNum(url):
    html = getPage(url)
    soup = BeautifulSoup(html,'lxml')
    end = soup.select('#txtPage')[0].get('value')
    num = end.split('/')[1]
    return num


def start(url):
    start_time = time.time()
    html = getPage(url)
    parse = parsePage(html)
    saveDB(parse)
    end_time = time.time()
    print('本次耗时： %s' % (end_time - start_time))


if __name__ == '__main__':
    pool = Pool(8)
    urls = ['http://m.xdingdiann.com/sort/1/{}.html'.format(num) for num in range(1, 11)]
    for url in urls:
        print(url)
        pool.apply_async(start(url))
        time.sleep(randint(3,5))
    pool.close()
    pool.join()
    print('工作完成！')
