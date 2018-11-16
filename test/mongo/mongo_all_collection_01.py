from collections import defaultdict

import pymongo


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "LianJia"
db_coll = db[COLLECTION ]

collections = db.list_collection_names()
# print(collections)
urls = list()
for coll in collections:
    if 'Task' in coll:
        db_coll = db[coll]
    num = db_coll.find({})
    i = 0
    while True:
        try:
            item = num.next()
            i+=1
            urls.append(item['community_url'])
            # print(item['community_url'])
            print(i)
        except StopIteration:
            break

print(len(urls))

