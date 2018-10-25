import requests
from bs4 import BeautifulSoup
import urllib.request
import pymongo
from multiprocessing import Pool

mongo_client = pymongo.MongoClient('localhost',27017)
db = mongo_client['spider_db']
qcdb = db.client['qcdb']


host = 'http://www.qcenglish.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host': 'www.qcenglish.com',
    'Referer': host
}

download_path = './tmp//'

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
    conunter = 1
    try:
        urllib.request.urlretrieve(url, file_path)
    except urllib.error.URLError as e:
        while conunter <= 3:
            print("尝试重连，当前次数：" + str(conunter))
            download(url,title)
            conunter += 1
        pass
    print('下载完成.......')

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

def url_generator(page_id,page_sum):
    page_sum = page_sum + 1
    for y in range(1,page_sum):
        url = 'http://www.qcenglish.com/ebook/list_' +  str(page_id)  + '_{}.html'.format(str(y))
        get_item_url(url)
        print('文章页获取ing....')


# url_generator(54,12)


if __name__ == '__main__':
    p = Pool()
    for item in qcdb.url.find():
        item_status = item.get('status')
        item_url = item.get('item_url')
        if item_status == 0:
            print('当前内容页：' + item_url)
            try:
                p.apply_async(get_article(item_url))
                qcdb.url.update({'item_url':item_url},{"$set":{"item_url":item_url,"status":1}},multi=False)
            except:
                print('发现一个玄学问题!')
                bad_url = {
                    'badURL': item_url,
                    'status': 0
                }
                qcdb.badurl.insert(bad_url)
                print('已加入BadURL中，请注意查看！')
                pass
        else:
            print('已经爬取过了····')
    print("等待新的线程加入！")
    p.close()
    p.join()
    print('完成！\n')