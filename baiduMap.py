# coding:utf-8
import requests
import pandas as pd
from time import sleep

ak='8f3eda4c614058b2710a9cead93641e8'
# KeyWord=u'早教'
# City=u'北京市'
# Tag=u'教育培训'
# Page=0

def getJson(url):
    response = requests.get(url)
    status = response.status_code
    data = response.json()
    if status == 200:
        return data
    else:
        num = 1
        while num < 4:
            print('连接错误！尝试重新获取！ 当前获取次数:' + str(num))
            num += 1
            sleep(3)
            print(url)
            getJson(url)
        print('Error!')
        return None

def getNum(data):
    # num = 0
    if data == None:
        return None
    else:
        total = data['total']
        # results = data['results']
        if total > 20:
            # pageNum = total // 20
            pageNum = int((total + 20 - 1) / 20)
            print('共检索到' + str(total) + '数据,共计：' + str(pageNum) + '页!')
            return pageNum
        else:
            pageNum = 1
            return pageNum

def parseData(data):
    if data == None:
        print('data is None!')
    else:
        datalist = []
        results = data['results']
        for i in results:
            name = i['name']
            add = i['address']
            detail = i['detail_info']
            mapUrl = detail['detail_url']
            if i.__contains__('telephone') == True:
                tel = i['telephone']
            else:
                tel = None

            tempData = {
                'name': name,
                'address': add,
                'tel': str(tel),
                'mapUrl': str(mapUrl)
            }
            datalist.append(tempData)
        return datalist

if __name__ == '__main__':
    headers = ['name','address','tel','map']
    KeyWord = input('输入检索关键词： \n')
    Tag = input('输入分类标签： \n')
    City = input('检索城市（市）： \n')
    startUrl = 'http://api.map.baidu.com/place/v2/search?query=' + KeyWord + \
                '&tag=' + Tag + \
                '&region=' + City + \
                '&output=json' + \
                '&ak=' + ak + \
                '&scope=2&page_size=20' + \
                '& page_num=0'
    json = getJson(startUrl)
    pageNum = getNum(json)
    if pageNum == None:
        print('No page number!')
    else:
        for num in range(0,int(pageNum)):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + KeyWord + \
                '&tag=' + Tag + \
                '&region=' + City + \
                '&output=json' + \
                '&ak=' + ak + \
                '&scope=2&page_size=20' + \
                '& page_num=' + str(num)
            print('获取当前页码：' + str(num))
            data = getJson(url)
            sleep(5)
            datalist = parseData(data)
            save = pd.DataFrame(datalist)
            try:
                save.to_csv('./result.csv',header=headers,index=False,mode='a+',encoding='utf_8_sig')
            except UnicodeEncodeError:
                print('Encode Error！')
