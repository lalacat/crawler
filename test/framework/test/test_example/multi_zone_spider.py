# mongodb服务的地址和端口号
import pprint
import pymongo

mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "XiaoQu"
db_coll = db[COLLECTION ]

projectionFields = {'_id':False}  # 用字典指定
#queryArgs = {"total_zone_name":"pudong"}

searchRes = db_coll.find(projection=projectionFields)
#searchRes = db_coll.find()



for result in searchRes:
    for name,info in result.items():
        if name == "total_zone_name":
            S = SpiderGetFromSchedlue()
        else:
            print(name,info)