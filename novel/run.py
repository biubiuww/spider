from crawler_dd import SpiderDingdian
# from pymongo import MongoClient
import pymongo
import time,datetime

client = pymongo.MongoClient()
bookinfo = client.novelDB.bookinfo
chapters = client.novelDB.chapters

# books = db['info']


dingdian = SpiderDingdian()

def saveDB(db,items):
    if items == None:
        pass
    else:
        for item in items:
            if db.count_documents(item) == 0:
                db.insert_one(item)
            else:
                pass
        db.close

        # if dbname.insert_one(item,upsert=True):
        #     print(item['book_name'])
        # else:
        #     print('save error!')
