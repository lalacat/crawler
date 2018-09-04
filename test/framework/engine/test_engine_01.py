from test.framework.engine.test_engine import ExecutionEngine
from test.framework.https.request import Request
from test.framework.setting import Setting
from test.framework.crawler import Crawler
from test.framework.https.request import Request
from spider.test_Spider_01 import Test_Spider_1
from twisted.internet import reactor
import logging

def finish_crawl(self, content, req):
    logging.info("finish")
    return content

settings = Setting()
crawler = Crawler(Test_Spider_1,settings)
spider = crawler._create_spider()
