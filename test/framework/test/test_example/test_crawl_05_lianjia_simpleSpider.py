from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor, defer
from test.framework.test.test_spider.simple_spider_02_xiaoqu import SimpleSpider

import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)
def finish_crawl(content,spider):
    logging.info("finish===>%d"%spider._item_num)
    print(spider._total_house)
    return



settings = Setting()
crawler_01 = Crawler(SimpleSpider,settings)
crawler_01.crawl()
reactor.run()