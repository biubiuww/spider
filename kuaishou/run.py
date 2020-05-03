from kuaishou.lib.crawler import Kuaishou



if __name__ == '__main__':

    with open('config/user.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            Kuaishou(i)
            Kuaishou.User()


