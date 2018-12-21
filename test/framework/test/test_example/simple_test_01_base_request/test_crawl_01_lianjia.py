from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor, defer
import logging

from test.framework.test.test_example.simple_test_01_base_request.lianjia_spider_simpletest import LJSpider

LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
def finish_crawl(content,spider):
    logging.info("finish===>%d"%spider._item_num)
    print(spider._total_house)
    return



settings = Setting()
crawler_01 = Crawler(LJSpider,settings)
c1 = crawler_01.crawl()
dd = defer.DeferredList([c1])
dd.addCallback(finish_crawl,crawler_01.spider)
dd.addBoth(lambda _:reactor.stop())
reactor.run()