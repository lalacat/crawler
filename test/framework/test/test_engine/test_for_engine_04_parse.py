from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from test.framework.spider.test_spider.test_Spider_01 import Test_Spider_1
from twisted.internet import reactor, defer
import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
def finish_crawl( content):
    logging.info("finish")
    return content



settings = Setting()
crawler_01 = Crawler(Test_Spider_1,settings)
spider_01 = crawler_01._create_spider()
c1 = crawler_01.crawl()
dd = defer.DeferredList([c1])
dd.addBoth(lambda _:reactor.stop())
reactor.run()