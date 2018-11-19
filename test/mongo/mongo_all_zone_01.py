from collections import defaultdict
import pprint

import pymongo


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
# COLLECTION = "XiaoQu"
COLLECTION = "Total Zone"
db_coll = db[COLLECTION]

searcher = db_coll.find({},{'part_zone_url':1,'_id':0})

while True:
    try:
        result = searcher.next()
        print(pprint.pformat(result))
    except StopIteration:
        print('没了')
        break