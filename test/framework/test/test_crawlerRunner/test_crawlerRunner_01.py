from collections import Iterable

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
COLLECTION = "XiaoQu"

xiaoqu = db[COLLECTION].find({})
# print(type(xiaoqu))
# print(xiaoqu)
one = xiaoqu.next()
# print(one)
# print(type(one))
db_coll = db[COLLECTION ]

collections = db.list_collection_names()

def make_generator(obj):
    if isinstance(obj,Iterable):
        try:
            it = iter(obj)
            times = 0
        except Exception as e :
            print(e)
        while True:
            try:
                yield it.__next__()
            except StopIteration:
                return "over"
                break
    else:
        print('False')
j = 0
# for i in make_generator(collections):
#     j += 1
#     if j == 50 :
#         temp = i
#         print(type(i))
#         print(i)
#     print(str(j)+':'+i)
a = make_generator(collections)
while True:
    try:
        for i in range(50):
            try:
                temp = next(a)
                print(temp)
            except StopIteration:
                print('没了')
                raise StopIteration('Nothing')
        print('50次\n')
    except StopIteration:
        break

