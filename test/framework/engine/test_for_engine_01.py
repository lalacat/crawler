from spider.test_Spider_02 import Test_Spider_2
from spider.test_Spider_03 import Test_Spider_3
from test.framework.engine.test_engine import ExecutionEngine
from test.framework.https.request import Request
from test.framework.setting import Setting
from test.framework.crawler import Crawler
from test.framework.https.request import Request
from spider.test_Spider_01 import Test_Spider_1
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
crawler_02 = Crawler(Test_Spider_2,settings)
crawler_03 = Crawler(Test_Spider_3,settings)
spider_01 = crawler_01._create_spider()
spider_02 = crawler_02._create_spider()
spider_03 = crawler_03._create_spider()
c1 = crawler_01.crawl()
c2 = crawler_02.crawl()
c3 = crawler_03.crawl()
dd = defer.DeferredList([c1,c2,c3])
dd.addBoth(lambda _:reactor.stop())
reactor.run()