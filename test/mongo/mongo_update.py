from collections import defaultdict

import pymongo


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "test"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "getPage_Collection"
db_coll = db[COLLECTION ]



_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
house_info = {'community_name': '和平花苑', 'community_url': 'https://sh.lianjia.com/xiaoqu/5011000017889/',
              'community_sale_num': '1', 'community_rent_num': '1',
              'community_onsale_num': '10',
              'community_bulid_year': '1997年建成',
              'community_avr_price': '75616'}
post_data = defaultdict(list)
post_data["A"] = [x for x in range(3)]
post_data["B"] = [x for x in range(3,6)]
post_data["C"] = [x for x in range(6,9)]
# result = db_coll.insert(post_data)
#  update(<query>,<update>,<upsert>,<multi>),其中<query>表示筛选的条件，<update>是要更新的数据

# db_coll.update({'author': 'Scott'},{'$set':{'grade':99}})
# 定位操作符(“$”)作为第一个匹配查询条件的元素的占位符，也就是在数组中的索引值
# db_coll.update({'A': 0 },{'$set':{'A.$':99}})
# 如果指定的键已经存在，会向已有的数组末尾加入一个元素，要是没有就会创建一个新的数组。
# db_coll.update({'A': 0},{'$push':{'A':{"$lt":99}}})
db_coll.update({'B': 3},{'$push':{'B':99}})

a = db_coll.find({})
for i in a:
   print(i)