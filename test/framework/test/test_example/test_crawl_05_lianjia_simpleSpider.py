from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor, defer
from test.framework.test.test_spider.simple_spider_03_allurl import SimpleSpider

import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.WARNING,format=LOG_FORMAT,datefmt=DATE_FORMAT)




settings = Setting()
crawler_01 = Crawler(SimpleSpider,settings)
c1 = crawler_01.crawl()
c1.addBoth(lambda _:reactor.stop())
reactor.run()