import requests
import pdfkit
from time import sleep
from bs4 import BeautifulSoup

'''
No.1 手痒撸的，单次只能下载一本，只能下载H5中内容自行合并PDF，不下载PDF。
No.2 token每小时都需要更新，获取方法自行网站中debug。
No.3 book ID not detail ID
No.4 感谢机械工业出版社......


'''

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=A6DF07780010F3F5D221497A3A345A8D',
    'DNT': '1',
    'Host': 'www.hzcourse.com',
    'Origin': 'http://www.hzcourse.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.hzcourse.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'http://www.hzcourse.com/web/refbook/queryAllChapterList'

path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wk)
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}

def getUrls(url,data):
    res = requests.post(url,data=data)
    jsdata = res.json()
    urls = []
    data = jsdata['data']
    for i in data['data']:
        link = i['ref']
        urls.append(link)
    return urls

def download(links):
    num = 1
    for i in links:
        xtm = requests.get(url = 'http://www.hzcourse.com/resource/readBook?path=' + str(i),headers=headers)
        soup = BeautifulSoup(xtm.text,'lxml')
        for img in soup.find_all('img'):
            img['src'] = 'http://www.hzcourse.com/resource/readBook?path=/openresources/teach_ebook/uncompressed/18563/OEBPS/Text/' + img['src']
        article = str(soup).encode('utf-8')
        with open(str(num) + '.html','wb') as f:
            f.write(article)
            f.close()
        try:
            pdfkit.from_file(str(num) + '.html',str(num) + '.pdf',configuration=config,options=options)
        except Exception as e:
            print('Error for ' + str(e) + ',Page :' + str(num))
        num += 1
        sleep(1)


if __name__ == '__main__':
    bookid = input("Please input bookid:")
    postData = {
        'ebookId': bookid,
        'token': '5a1536002e3441d0af4c3d640d0b37e9'
    }
    links = getUrls(url,postData)
    download(links)
