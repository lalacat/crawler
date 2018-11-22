
from collections import Iterable

import pymongo

from twisted.internet import reactor

from test.framework.setting import Setting
from test.framework.test.test_crawlerRunner.crawlerRunner_for_distribute_from_01 import CrawlerRunner

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
queryArgs = [
    {"total_zone_name":"putuo"},
    {"total_zone_name":"minhang"},
    {"total_zone_name":"xuhui"},
    {"total_zone_name":"baoshan"},
    {"total_zone_name":"yangpu"},
    {"total_zone_name":"songjiang"},
    {"total_zone_name":"changning"},
    {"total_zone_name":"pudong"},
    {"total_zone_name":"jiading"},
    {"total_zone_name":"zhabei"},
    {"total_zone_name":"fengxian"},
    {"total_zone_name":"jiangan"},
    {"total_zone_name":"hongkou"},
    {"total_zone_name":"qingpu"},
    {"total_zone_name":"huangpu"},
    ]

searchRes = db_coll.find({"total_zone_name":"putuo"},{'_id':False})

all_zone =[]
for query in queryArgs:
    search = db_coll.find(query,{'_id':False})
    while True:
        try:
            next_task = search.next()
            #  task_name = next_task["total_zone_name"][0]
            for name, url in next_task.items():
                if name != 'total_zone_name':
                    all_zone.append(url)
        except StopIteration:
            break

# print(len(all_zone))
# print(pprint.pformat(all_zone))





zone_name = "yangpu"
town_urls = [
    'https://sh.lianjia.com/xiaoqu/anshan/',# 157 156

    #'https://sh.lianjia.com/xiaoqu/dongwaitan/',# 144 141
    #'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',#159 159
    #'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    #'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    #'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    #'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    #'https://sh.lianjia.com/xiaoqu/zhongyuan1/'

]
town_urls_dict= [
    'https://sh.lianjia.com/xiaoqu/anshan/',# 157 156
    'https://sh.lianjia.com/xiaoqu/dongwaitan/',# 144 141
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',#159 159
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/',
]

s = Setting()
cr = CrawlerRunner(town_urls_dict,s)
d = cr.start()
d.addBoth(lambda _:reactor.stop())
# reactor.callLater(2,cr.stop)
reactor.run()



