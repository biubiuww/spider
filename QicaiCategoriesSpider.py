import requests
from bs4 import BeautifulSoup
import urllib.request
import pymongo
import time,random
from multiprocessing import Pool

mongo_client = pymongo.MongoClient('localhost',27017)
db = mongo_client['spider_db']
qcdb = db.client['qcdb']



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host': 'www.qcenglish.com',
    'Referer': 'http://www.qcenglish.com'
}

host = 'http://www.qcenglish.com'
download_path = './tmp//'

def get_item_url(url):
    print('当前URL： ' + url)
    wb_date = requests.get(url,headers=headers)
    wb_date.encoding = wb_date.apparent_encoding
    soup = BeautifulSoup(wb_date.text,'lxml')
    items = soup.select('#container > div.content > dl.listitem > a')
    for item in items:
        # item = item.get('href')
        data = {
            'item_url': host + item.get('href'),
            'status': 0
        }
        print(data)
        qcdb.url.insert(data)
    print('当前列表页爬取完成！\n')

def get_article(url):
    req = requests.get(url,headers=headers)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text,'lxml')
    try:
        pdf_title = soup.select('#details > dl > dd')[0].get_text()
        download_link = soup.select('#download > li > a')[0].get('href')
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
    print('延迟等待...')
    time.sleep(5)

def url_generator():
    for x in range(1,12):
        url = 'http://www.qcenglish.com/ebook/list_17_{}.html'.format(str(x))
        get_item_url(url)
        print('文章页获取ing....')
        time.sleep(3)


def run():
    for item in qcdb.url.find():
        item_status = item.get('status')
        item_url = item.get('item_url')
        flag = 1
        if item_status == 0:
            print('当前内容页：' + item_url)
            try:
                get_article(item_url)
                qcdb.url.update({'item_url':item_url},{"$set":{"item_url":item_url,"status":1}},multi=False)
                print('下载完成！')
            except TimeoutError as e:
                print('连接超时，错误代码：' + e)
                if flag <= 3:
                    print('尝试重连，当前次数：' + flag)
                    get_article(item_url)
                    flag += 1
                else:
                    bad_url = {
                        'badURL': item_url,
                        'status': 0
                    }
                    qcdb.badurl.insert(bad_url)
                    print('重连失败！已加入BadURL中，请注意查看！')
                    pass
        else:
            print('已经爬取过了····')

# item_urls = qcdb.url.find()
# for item_url in item_urls:
#     flag = 1
#     item_url = item_url.get('item_url')
#     print('当前URL为：' + item_url)
#     try:
#         get_article(item_url)
#     except TimeoutError as e:
#         print(e)
#         if flag <= 3:
#             print('尝试重连，第' + str(flag) + '次！')
#             get_article(item_url)
#             flag += 1
#             time.sleep(10)
#         else:
#             print('重连失败，跳过此链接！')
#             bad_url ={
#                 'bad_url':item_url
#             }
#             qcdb.url.insert(bad_url)
#             print('失败连接已存入数据库中，请注意查看！')
#             pass