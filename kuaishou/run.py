from lib.crawler import Kuaishou
from time import sleep
from config.user import users

file_list = []  #创建一个空列表
def out_file(input_file,out_file):
    with open(input_file, "r") as f:
        file_2 = f.readlines()
        for file in file_2:
            file_list.append(file)
        out_file1 = set(file_list)    #set()函数可以自动过滤掉重复元素
        last_out_file = list(out_file1)
        for out in last_out_file:
            with open(out_file,"a+",encoding="utf-8") as f:   #去重后文件写入文件里
                f.write(out)
                print(out)

def run():
    app = Kuaishou()
    for i in users:
        app.setUid(i)
        sleep(10)

    out_file('data/data.txt', 'data.txt')

if __name__ == '__main__':
    run()
