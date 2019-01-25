import time

import pymongo


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LOG"
db = client[DATABASE]
# db.
# temp = db.list_collection_names()
#
# print(temp)

#连接到集合(表):myDatabase.myCollection
COLLECTION = '01/23/2019'
db_coll = db[COLLECTION ]

# projectionFields = {'_id':False}  # 用字典指定
# queryArgs = {"total_zone_name":"pudong"}
#
# searcher = db_coll.find({})
#
# while True:
#     try:
#         dict = searcher.next()
#         print(len(dict))
#     except StopIteration:
#         break

bulid_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
base_date = {'bulid_time': bulid_time}
db_coll.insert(base_date)
l = len(db_coll.find(base_date).next())
print(l)
id = db_coll.find(base_date).next()['_id']

from bson import ObjectId

for i in range(100):
    l =len(db_coll.find({'_id':ObjectId(id)}).next())
    if l <10:
        db_coll.update({'_id':ObjectId(id)},{'$set':{str(i):i}})
    else:
        bulid_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        base_date = {'bulid_time': bulid_time}
        db_coll.insert(base_date)
        id = db_coll.find(base_date).next()['_id']