import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from functools import reduce
import time,datetime

'''
 sort_id 定义分类
 
  默认爬取前200页
 
'''

class SpiderDingdian():



    def sort(self,url):
        sortlist = [
            {
                'sortid': 1,
                'name': '玄幻奇幻'
            },
            {
                'sortid': 2,
                'name': '武侠仙侠'
            },
            {
                'sortid': 3,
                'name': '都市言情'
            },
            {
                'sortid': 4,
                'name': '历史军事'
            },
            {
                'sortid': 5,
                'name': '科幻灵异'
            },
            {
                'sortid': 6,
                'name': '网游竞技'
            },
            {
                'sortid': 7,
                'name': '女生频道'
            }
        ]
        sortid = int(url.split('/')[-2])
        for sort in sortlist:
            if sortid == sort['sortid']:
                name = sort['name']
                return name
            else:
                name = '未定义'
                return name

    def get_page(self,url):
        UA = UserAgent()
        headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': UA.random
        }
        try:
            req = requests.get(url,headers=headers)
            req.raise_for_status()
            req.close()
            req.encoding = req.apparent_encoding
            page = BeautifulSoup(req.text,'lxml')
            return page
        except:
            return

    def bookinfo(self):
        info = []
        page = self.get_page(self.url)
        if page == None:
            return
        else:
            sortname = self.sort(self.url)
            items = page.select('div.hot_sale')
            for item in items:
                data = {
                    'book_id': item.select('div.bookinfo > a')[0].get('href').split('/')[-2],
                    'book_pic': item.select('div.bookimg > a > img')[0].get('data-original'),
                    'book_name': item.select('div.detail > p.title')[0].get_text(),
                    'author': item.select('p.author')[0].get_text().strip('作者：'),
                    'score': item.select('div.score')[0].get_text(),
                    'book_desc': item.select('p.review')[0].get_text().split('简介：')[1].strip(),
                    'sort':sortname
                }
                info.append(data)
            return info

    def chapter(self):
        chapters = []
        page = self.get_page(self.url)
        if page == None:
            return
        else:
            book_id = self.url.split('/')[-2]
            items = page.select('#list > dl > dd > a')
            for item in items:
                data = {
                    'book_id':book_id,
                    'chapter_id': item.get('href').split('/')[-1].strip('.html'),
                    'name': item.get_text()
                }

                chapters.append(data)
            run_function = lambda x, y: x if y in x else x + [y]
            return reduce(run_function, [[], ] + chapters)

    def content(self):
        page = self.get_page(self.url)
        if page == None:
            return
        else:
            bookname = page.select('div.bookname > h1')[0].get_text()
            # item= page.select('#content')[0]
            content = page.find('div',attrs={'id':"content"}).text
            content = content.replace('\t','')
            content = content.replace('　　','\r\n')
            content = content.replace('chaptererror();','')
            data = {
                'bookname':bookname,
                'content':content,
            }
            return data


