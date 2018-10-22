import pymongo

from test.framework.test.test_spider.lianjia_spider.lianjia_spider_total_community_db import Part_Zone
from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor
import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)


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
scheduler = searchRes.next()


settings = Setting()
crawler_01 = Crawler(Part_Zone,settings)
crawler_01._create_spider()
c1 = crawler_01.crawl()
c1.addBoth(lambda _:reactor.stop())
reactor.run()