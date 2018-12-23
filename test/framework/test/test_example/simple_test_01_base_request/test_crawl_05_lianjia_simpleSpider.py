from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor

from test.framework.test.test_example.simple_test_01_base_request.lianjia_spider_simpletest import LJSpider
from test.framework.test.test_spider.simple_spider.simple_spider_01_totalPageNumber import SimpleSpider_01

'''
LOG_FORMAT = '[%(levelname)s] [%(asctime)s]-[%(filename)s][line:%(lineno)d]: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)
'''




settings = Setting()
crawler_01 = Crawler(LJSpider,settings)
c1 = crawler_01.crawl()
c1.addBoth(lambda _:reactor.stop())
reactor.run()

