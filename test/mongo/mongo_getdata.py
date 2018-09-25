import pymongo


# mongodb服务的地址和端口号
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
queryArgs = {"total_zone_name":"pudong"}

searchRes = db_coll.find(queryArgs,projectionFields)

if searchRes:
    print("true")
    print(searchRes.count())
else:
    print("false")

for list in searchRes:
    for name,url in list.items():
        print(name,":",url)