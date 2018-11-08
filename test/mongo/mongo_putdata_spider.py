import pymongo
from framework.test import Part_Zone


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "Total Zone"
db_coll = db[COLLECTION ]

projectionFields = {'_id':False}  # 用字典指定
queryArgs = {"part_zone_name":"pudong"}

searchRes = db_coll.find(queryArgs,projectionFields)

#print(searchRes.count())
#d = searchRes.next()
spider = Part_Zone.from_schedule(searchRes.next())
for name in spider.start_requests():
    print(name)

