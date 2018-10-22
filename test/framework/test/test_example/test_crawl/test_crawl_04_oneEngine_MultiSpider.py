from test.framework.test.test_spider.lianjia_spider.lianjia_spider_total_community_db import Part_Zone
from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor

import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)

zone_name = "yangpu"
town_urls = [
    'https://sh.lianjia.com/xiaoqu/anshan/',
    'https://sh.lianjia.com/xiaoqu/dongwaitan/',
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/'
]



settings = Setting()
crawler_01 = Crawler(Part_Zone,settings)
c1 = crawler_01.crawl()
c1.addBoth(lambda _:reactor.stop())
reactor.run()