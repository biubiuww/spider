import os
import sys
import requests

host = 'https://1.yasee1.com/'

def getVideoId():
    videoId = int(input("Input Video ID: "))
    # videoUrl = host + str("video-") + str(videoId)
    return str(videoId)

def getXHR():
    videoId = getVideoId()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": str(host) + "video-" + str(videoId)
    }
    videoUrl = str(host) + "index/req/getPlayerDomain?id=" + videoId
    response = requests.get(videoUrl,headers=headers)
    res_status = response.status_code
    if res_status == 200:
        response = response.json()
        # print(response)
        return response
    else:
        return None

def parseXHR():
    XHR = getXHR()
    code = XHR.get("code")
    if code == -2:
        data = XHR.get("info")
        down_url = data.get("down_url")
        video_hls = data.get("video_hls")
        data = {
            "down_url" : down_url,
            "video_hls" : video_hls
        }
        return data
    else:
        print('Error! \n')
        return None


def m3u8(data):
    down_url = data.get("down_url")
    video_hls = data.get("video_hls")
    hlsUrl = video_hls.split('/',3)

    if hlsUrl[2] == '[domain_dan]':
        video_hls = video_hls.replace("[domain_dan]","hone.yyhdyl.com")
    elif hlsUrl[2] == '[domain_fourth]':
        video_hls = video_hls.replace("[domain_fourth]","head2.yyhdyl.com")
    elif hlsUrl[2] == '[domain_shuang]':
        video_hls = video_hls.replace("[domain_shuang]","htwo.yyhdyl.com")
    elif hlsUrl[2] == '[domain_three]':
        video_hls = video_hls.replace("[domain_three]","head.yyhdyl.com")
    else:
        video_hls = None

    if down_url == None:
        return video_hls
    else:
        quality = down_url[-9:-5]
        if quality == str("720p"):
            video_hls = video_hls.replace("hls.m3u8","hls-720p.m3u8")
        elif quality == str("480p"):
            video_hls = video_hls.replace("hls.m3u8","hls-480p.m3u8")
        elif quality == str("360p"):
            video_hls = video_hls.replace("hls.m3u8","hls-360p.m3u8")
        elif quality == str("240p"):
            video_hls = video_hls.replace("hls.m3u8","hls-240p.m3u8")
        else:
            video_hls = None
    return video_hls

def download(url,filename):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
    downloadPath = os.getcwd() + '\Temp'
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    content = requests.get(url,headers=header).text
    num = 0
    tempVideo = os.path.join(downloadPath,f'{filename}.ts')
    fileLine = content.split('\n')
    for line in fileLine:
        if line[-4:] == ".jpg":
            tsUrl = url.rsplit('/',1)[0] + "/" + line
            # res = requests.get(tsUrl)
            # with open(downloadPath + "\\" + str(num) + ".ts",'wb') as f:
            #     f.write(res.content)
            #     f.flush()
            print(tsUrl)
            num += 1
    print('Download Successful!')



if __name__ == '__main__':
    while True:
        XHR = parseXHR()
        if XHR == None:
            print('Error!\n')
        else:
            m3u8_url = m3u8(XHR)
            print(m3u8_url)
