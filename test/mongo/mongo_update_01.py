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
COLLECTION = "test_lianjia"
db_coll = db[COLLECTION ]



_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
house_info = {'community_name': '和平花苑', 'community_url': 'https://sh.lianjia.com/xiaoqu/5011000017889/',
              'community_sale_num': ['1'], 'community_rent_num': ['1'],
              'community_onsale_num': ['10'],
              'community_bulid_year': '1997年建成',
              'community_avr_price': '75616'}
house_info_01 = {'community_name': '和平花苑', 'community_url': 'https://sh.lianjia.com/xiaoqu/5011000017889/',
              'community_sale_num': '10', 'community_rent_num': '5',
              'community_onsale_num': '12',
              'community_bulid_year': '1997年建成',
              'community_avr_price': '75616'}
house_info_02 = {'community_name': '和平花苑', 'community_url': 'https://sh.lianjia.com/xiaoqu/5011000017889/',
              'community_sale_num': '112', 'community_rent_num': '5',
              'community_onsale_num': '133',
              'community_bulid_year': '1997年建成',
              'community_avr_price': '75616'}

#  update(<query>,<update>,<upsert>,<multi>),其中
# <query>表示筛选的条件
# update : update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的
# upsert : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。
# multi : 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新。
# writeConcern :可选，抛出异常的级别。
# 定位操作符(“$”)作为第一个匹配查询条件的元素的占位符，也就是在数组中的索引值
# db_coll.update({'A': 0 },{'$set':{'A.$':99}})
# 如果指定的键已经存在，会向已有的数组末尾加入一个元素，要是没有就会创建一个新的数组。

# db_coll.insert(house_info)

# a = db_coll.find(house_info).count()
# print(a)
# b = db_coll.find({'community_name':house_info_01['community_name']}).count()
# # print(b)
db_coll.update({'community_name':house_info_01['community_name']},
               {'$set':{
                   'community_sale_num': house_info_01['community_sale_num'],
                   'community_rent_num': house_info_01['community_rent_num'],
                   'community_onsale_num': house_info_01['community_onsale_num'],
                   'community_avr_price': house_info_01['community_avr_price']
                }},
               multi=True)


# def db_filter(item):
#     print(type(item))
#     #  1.防止重复写入
#     #  2.对某条字段更新
#     num_01 = db_coll.find(item).count()
#     print(num_01)
#     print(type(num_01))
#     num_02 = db_coll.find({'community_name':item['community_name']}).count()
#     print(num_02)
#     print(type(num_02))
#
#     # if num_01 == 1:
#     #     return 'exist'
#     # elif num_02 == 1:
#     #     return 'update'
#     # else:
#     #     return 'insert'
#
#
#
# a = db_filter(house_info_02)
# print(a)