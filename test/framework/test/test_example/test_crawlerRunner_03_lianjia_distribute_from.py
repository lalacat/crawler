import logging
from typing import Iterable

import pymongo
import queue

from twisted.internet import reactor

from test.framework.setting import Setting
from test.framework.test.test_crawler.test_crawlerRunner_from import CrawlerRunner

LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.CRITICAL,format=LOG_FORMAT,datefmt=DATE_FORMAT)




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
queryArgs = {"total_zone_name":"jingan"}

searchRes = db_coll.find(queryArgs,{'_id':False})



zone_name = "yangpu"
town_urls = [
    'https://sh.lianjia.com/xiaoqu/anshan/',# 157 156

    'https://sh.lianjia.com/xiaoqu/dongwaitan/',# 144 141
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',#159 159
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/'

]


s = Setting()
cr = CrawlerRunner.task_from(searchRes)
d = cr.start()
d.addBoth(lambda _:print(_))
d.addBoth(lambda _:reactor.stop())
reactor.run()

