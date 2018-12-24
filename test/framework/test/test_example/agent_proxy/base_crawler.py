from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor, defer
import logging

from test.framework.test.test_example.agent_proxy.simple_spider_proxy import LJSpiderProxy

def finish_crawl(content,spider):
    logging.info("finish===>%d"%spider._item_num)
    return



settings = Setting()
crawler_01 = Crawler(LJSpiderProxy,settings)
c1 = crawler_01.crawl()
dd = defer.DeferredList([c1])
dd.addCallback(finish_crawl,crawler_01.spider)
dd.addBoth(lambda _:reactor.stop())
reactor.run()

