# mongodb服务的地址和端口号
import pymongo
from test.framework.test import SpiderGetFromSchedlue

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


spiders = []
''''''
for result in searchRes:
    s = SpiderGetFromSchedlue()
    urls = []
    for name,info in result.items():
        if name == "total_zone_name":
            s.name = info[0]
        else:
            urls.append(info)
    s.start_urls = urls
    spiders.append(s)

for spider in spiders:
    print(spider.name)
    print(spider.start_urls)