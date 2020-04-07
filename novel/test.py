from crawler_dd import SpiderDingdian
import pymongo
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re

client = pymongo.MongoClient()
bookinfos = client.novelDB.bookinfo
chapters = client.novelDB.chapter
contents = client.novelDB.content
dingdian = SpiderDingdian()
UA = UserAgent()

headers = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': UA.random
}

def saveDB(db,items):
    if items == None:
        pass
    else:
        for item in items:
            if db.count_documents(item) == 0:
                db.insert_one(item)
            else:
                pass
        db.close

def test_bookinfo():
    num = 0
    urls = ['http://m.xdingdiann.com/sort/1/{}.html'.format(n) for n in range(1,3)]
    for url in urls:
        num += 1
        dingdian.url = url
        info = dingdian.bookinfo()
        saveDB(bookinfos,info)
        print('第 %s 次测试完成！')
    print('done \n')

def test_chapter():
    dingdian.url = 'http://www.xdingdiann.com/ddk204240/'
    chapter = dingdian.chapter
    saveDB(chapters,chapter)
    print('done! \n')

def test_content():
    dingdian.url = 'http://www.xdingdiann.com/ddk204240/1067630.html'
    content = dingdian.content()
    temp = [content]
    # saveDB(contents,content)
    saveDB(contents,temp)
# test_content()
w_path = './'
url = 'http://www.xdingdiann.com/ddk204240/1067630.html'
req = requests.get(url,headers=headers)

'''

content = re.findall(r'<div id="content">(.*?)</div>', req.text, re.S)[0]
content = content.replace('<br/>', '\r').replace(' ', '').replace('<p>', '').replace('</p>', '').replace('<script>','').replace('</script>','').replace('chaptererror();','')
'''
page = BeautifulSoup(req.text,'lxml')
content = page.find('div', attrs={'id': "content"}).text
content = content.replace('\t', '')
content = content.replace('　　', '\r\n')
content = content.replace('chaptererror();', '').strip()
temp = url.split('/')
book_id = temp[-2].strip()
content_id = temp[-1].replace('.html','.txt')
filename = w_path + book_id + '/' + content_id
with open(filename,'w',encoding='utf-8') as f:
    f.write(content)
    f.close()
# print(content)
print(filename)

'''
太监判断：
1、更新时间 ＞ 90天
2、章节是否包含 大结局
'''