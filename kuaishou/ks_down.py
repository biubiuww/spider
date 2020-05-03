import requests
from multiprocessing import Pool
from fake_useragent import UserAgent
import time
import os


video_path ='./video/'

UA = UserAgent()

headers = {
    'Connection': 'close',
    'User-Agent':UA.random
}

def download(url):
    video_name = url[-24:]
    if os.path.exists(video_path+video_name) == True:
        print(video_name + ' 视频已存在，跳过')
        pass
    else:
        try:
            req = requests.get(url,headers=headers)
            req.raise_for_status()
            req.close()
            with open(video_path + video_name,'wb') as f:
                f.write(req.content)
                f.close()
            print(str(video_name) + ' ~下载完成！')
        except Exception as code:
            print(code)
            return None

if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(8)
    with open('./20200320.txt', 'r') as f:
        for line in f:
            line = line.split('?')[0]
            line = line.strip('/\n')
            pool.apply_async(download(line))
        pool.close()
        pool.join()

    end_time = time.time()
    print('下载完成，总耗时：%s' % (end_time - start_time))