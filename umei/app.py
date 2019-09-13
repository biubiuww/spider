import requests
import sys, os
from bs4 import BeautifulSoup
from time import sleep

urls = ['https://www.umei.fun/categories/16?page={}'.format(str(i)) for i in range(1,63)]
cookie = ''

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

def respon(url):
    response = requests.get(url,headers=headers)
    status = response.status_code
    if status == 200:
        return response.text
    else:
        return None

def gerUrls(page):
    if page == None:
        print('None!')
    else:
        # urllist = []
        html = BeautifulSoup(page,'lxml')
        urls = html.select('div.section-white > div > div > div > div > div > div > div > a')
        for url in urls:
            url = 'https://www.umei.fun' + url.get('href')
        #     urllist.append(url)
        # return urllist
            imgpage = respon(url)
            getImg(imgpage)

def getImg(page):
    html = BeautifulSoup(page,'lxml')
    imgs = html.select('div.container > div > div > img')
    title = html.select('h2')[0].get_text()
    if imgs == []:
        print('No img!')
        pass
    else:
        for img in imgs:
            img = img.get('src')
            download(img,title)
        print(str(title) + ' download succesful!')


def download(url,title):
    picPath = os.getcwd() + '\pic' + '\\' + str(title)
    if not os.path.exists(picPath):
        os.mkdir(picPath)
    con = requests.get(url)
    name = url[-8:]
    with open(picPath + '\\' + str(name) + '.jpg','wb') as f:
        f.write(con.content)
        f.flush()

# t1 = respon('https://www.umei.fun/posts/7308')
# getImg(t1)
if __name__ == '__main__':
    for url in urls:
        print(url)
        try:
            res = respon(url)
            imgUrls = gerUrls(res)
            sleep(1)
        except:
            print('Error \n')
            continue
