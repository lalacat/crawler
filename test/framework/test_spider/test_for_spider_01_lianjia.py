from spider.lianjia_spider_01 import LJSpider
from test.framework.middleware.test_process_item_01 import Test_Process_item_A
from test.framework.setting import Setting
from test.framework.crawler import Crawler
from spider.test_Spider_01 import Test_Spider_1
from twisted.internet import reactor, defer
import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
def finish_crawl(content,spider):
    logging.info("finish===>%d"%spider._item_num)
    print(spider._total_house)
    return



settings = Setting()
crawler_01 = Crawler(LJSpider,settings)
#spider_01 = crawler_01.spidercls()
c1 = crawler_01.crawl()
dd = defer.DeferredList([c1])
dd.addCallback(finish_crawl,crawler_01.spider)
dd.addBoth(lambda _:reactor.stop())
reactor.run()