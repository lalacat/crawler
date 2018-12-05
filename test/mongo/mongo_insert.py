import re
from collections import defaultdict

import pymongo

# mongodb服务的地址和端口号
from bson import ObjectId

mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "test"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "test_lianjia"
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


c =    { '密云小区 3室1厅 76.05平米': {'sold_address': '南 | 其他\xa0| 无电梯',
                                   'sold_dealDate': '2015.11.01',
                                   'sold_dealcycle': '成交周期678天',
                                   'sold_positionInfo': '中楼层(共6层) 1992年建板楼',
                                   'sold_saleonborad': '挂牌370万',
                                   'sold_totalPrice': '330',
                                   'sold_unitPrice': '43393'},
             '密云小区 3室1厅 79.4平米': {'sold_address': '南 | 精装\xa0| 无电梯',
                                  'sold_dealDate': '2018.05.09',
                                  'sold_dealcycle': '成交周期335天',
                                  'sold_positionInfo': '高楼层(共6层) 1990年建板楼',
                                  'sold_saleonborad': '挂牌595万',
                                  'sold_totalPrice': '558',
                                  'sold_unitPrice': '70278'}}
# item = {}
# for key in c.keys():
#     item[key.replace('.','_')] = c[key]
#
# print(item)
# result = db_coll.insert(item)
#
# a = db_coll.find({'_id':ObjectId("5c07cd0889088171a04b0ccf")},{'_id':False})
#
# b = a.next()
# print(b)
a = {'_id': ObjectId('5c07e0738908814f34dfc148'),
 'community_name': 'Task_sold_鞍山三村',
 '鞍山三村 1室0厅 31_67平米146.8': {
    'sold_address': '南 北 | 简装\xa0| 无电梯',
    'sold_dealDate': '2018.10.29',
    'sold_totalPrice': '386',
    'sold_unitPrice': '62908',
    'sold_positionInfo': '中楼层(共5层) 2002年建板楼',
    'sold_saleonborad': '挂牌395万',
    'sold_dealcycle': '成交周期136天'
    },
 '鞍山三村 2室0厅 47_18平米': {
     'sold_address': '南 | 其他\xa0| 无电梯',
     'sold_dealDate': '2017.06.23',
     'sold_totalPrice': '350',
     'sold_unitPrice': '74184',
     'sold_positionInfo': '低楼层(共5层) 2002年建板楼',
     'sold_saleonborad': '挂牌360万',
     'sold_dealcycle': '成交周期773天'},
 '鞍山三村 1室0厅 23_86平米': {
     'sold_address': '暂无数据 | 其他\xa0| 无电梯',
     'sold_dealDate': '2017.01.18',
     'sold_totalPrice': '185',
     'sold_unitPrice': '77536',
     'sold_positionInfo': '中楼层(共5层) 2002年建板楼',
     'sold_saleonborad': '挂牌190万',
     'sold_dealcycle': '成交周期617天'},
 }
d = {
    "鞍山三村 1室0厅 31_67平米146":'a',
    '鞍山三村 1室0厅 31_67平米146':'b'
}

# b = d.keys() - a.keys()
# print(b)


item = {
    'a':1,
    'a':2,
    'a':3
}

db_coll.insert(item)