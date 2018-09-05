from spider.test_Spider_02 import Test_Spider_2
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

def start_request_01():
    start_url = list()
    url = 'https://www.smzdm.com/homepage/json_more?p='

    for i in range(100):
        i = str(i)
        u = url + i
        start_url.append(u)

    for url in start_url:
        #print(url)
        yield Request(url)

settings = Setting()
crawler_01 = Crawler(Test_Spider_1,settings)
spider1 = crawler_01._create_spider()

engine = ExecutionEngine(crawler_01,finish_crawl)
downloads = []
for request in start_request_01():
    #(request.url)
    agent = engine._download(request,spider1)
    #agent.addCallback(request_callback)
    downloads.append(agent)
dd1 = defer.DeferredList(downloads)
dd1.addBoth(lambda _: reactor.stop())

reactor.run()