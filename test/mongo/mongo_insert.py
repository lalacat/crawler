from collections import defaultdict

import pymongo

# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "Twisted_Database"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "getPage_Collection"
db_coll = db[COLLECTION ]


"""  
post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
"""
post_data = defaultdict(list)
post_data["A"] = [x for x in range(3)]
post_data["B"] = [x for x in range(3,6)]
post_data["C"] = [x for x in range(6,9)]
#  result = db_coll.insert(post_data)
a = db_coll.find({})
for i in a:
   for l,j in i.items() :
       print(l,j)