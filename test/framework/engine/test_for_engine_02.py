from spider.test_Spider_02 import Test_Spider_2
from spider.test_Spider_03 import Test_Spider_3
from test.framework.engine.test_engine_01 import ExecutionEngine
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

    for i in range(10):
        i = str(i)
        u = url + i
        start_url.append(u)

    for url in start_url:
        #print(url)
        yield Request(url)
def start_request_02():
    start_url = list()
    url = 'https://www.smzdm.com/homepage/json_more?p='

    for i in range(10,20):
        i = str(i)
        u = url + i
        start_url.append(u)

    for url in start_url:
        #print(url)
        yield Request(url)
def start_request_03():
    start_url = list()
    url = 'https://www.smzdm.com/homepage/json_more?p='

    for i in range(20,30):
        i = str(i)
        u = url + i
        start_url.append(u)

    for url in start_url:
        #print(url)
        yield Request(url)

def print_err(content):
    print(content)
    return content

settings = Setting()
crawler_01 = Crawler(Test_Spider_1,settings)
crawler_02 = Crawler(Test_Spider_2,settings)
crawler_03 = Crawler(Test_Spider_3,settings)
spider1 = crawler_01._create_spider()
spider2 = crawler_02._create_spider()
spider3 = crawler_03._create_spider()

engine_01 = ExecutionEngine(crawler_01,finish_crawl)
engine_02 = ExecutionEngine(crawler_01,finish_crawl)
engine_03 = ExecutionEngine(crawler_01,finish_crawl)
start_requests=[start_request_01(),start_request_02(),start_request_03()]
engines = [engine_01,engine_02,engine_03]
downloads = []
for start_request,engine in zip(start_requests,engines):
    #(request.url)
    engine.start()
    crawl = engine.open_spider(spider1,start_request)
    #agent.addCallback(request_callback)
    downloads.append(crawl)
dd1 = defer.DeferredList(downloads)
dd1.addErrback(print_err)
dd1.addBoth(lambda _: reactor.stop())

reactor.run()