import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from datetime import datetime
from time import sleep
from random import randint

FILE_PATH = './'

host = 'https://www.cableav.tv/'

proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890'
}
ua = UserAgent()
headers = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "zh-CN,zh;q=0.9",
  "cache-control": "max-age=0",
  "dnt":"1",
  "referer":"https://cableav.tv/playlist/",
  "user-agent": ua.random
}

def open_page(url):

  sleep(randint(1,3))
  print('\n{} - [INFO]: requests at {}'.format(
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),url))

  req = requests.get(url,headers=headers,proxies=proxies)
  try:
    if req.status_code == 200 or req.status_code == 304:
      req.encoding = 'utf-8'
      return req
  except TimeoutError:
    print("Timeout:")
    cnt = 0
    while cnt < 3:
      open_page(url)
      cnt += 1

def parse_playlist(html):

  if html != None:
    page = BeautifulSoup(html.text,'lxml')
    video_urls = page.select('div.listing-content > h3 > a')
    for i in video_urls:
      data = i.get('href')
      yield data
  else:
    print("Result is None! \n")
    pass

def parse_video(html):
  PATTERN_URL = r'.*\"single_media_sources\":(\[\{.*\}\])'
  if html != None:
    page = BeautifulSoup(html.text,'lxml')
    m3u8 = page.find("meta", {"property": "og:video:url"})["content"]
    video_tags = page.find_all("meta", {"property": "video:tag"})
    best_quality = max([int(tag["content"][: -1]) for tag in video_tags])
    title = page.find("title").text.replace(' - CableAV','')

    for line in html.text.split('\n'):
      match = re.match(PATTERN_URL, line)
      if match:
        quality_lists = eval(match.group(1))
        for quality in quality_lists:
          if str(best_quality) in quality['source_label']:
            m3u8 = quality['source_file'].replace('\/', '/')
            break
  # return [title,m3u8]
    save_file(title,m3u8)


def save_file(title,m3u8):
  try:
    with open(FILE_PATH + 'test.txt','ab+') as f:
      result = '{},{}\r\n'.format(title,m3u8)
      f.write(result.encode('utf-8'))
    f.close()
  except IOError as e:
    print(e)
    pass

def run(url):
  page = open_page(url)
  play_list = parse_playlist(page)
  for i in play_list:
    video_page = open_page(i)
    parse_video(video_page)

if __name__ == '__main__':
  while True:
    start_url = input("Input page URL: \n")
    page_num = int(input('Input page list num：\n'))
    if page_num <= 1:
      run(start_url)
    else:
      urls = [start_url + "page/" + "{}/".format(x) for x in range(2,page_num+1)]
      run(start_url)
      for url in urls:
        run(url)
