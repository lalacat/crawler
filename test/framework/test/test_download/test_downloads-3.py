from test.framework.core.crawler import Crawler
from test.framework.downloads import Downloader
from test.framework.setting import Setting
from test.framework.https.request import Request
from spider.spider1 import Spider1
from twisted.internet import reactor, defer
import logging

headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]}
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)

def request_callback(content):
    print("request_and_response callback")
    print(content)

    return content.body


def request_errback(content):
    print("request_and_response errback")
    print(content[1])
    return content

def agent_print(content):
    print("agent_print")
    print(type(content))
    print(content)


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


settings = Setting()
crawler = Crawler(Spider1,settings)
spider = crawler._create_spider()
downloader_01 = Downloader(crawler)
downloader_02 = Downloader(crawler)

"""
httphandler = HTTPDownloadHandler(settings)
agent = httphandler.download_request(request,spider)
agent.addCallback(agent_print)
agent.addErrback(request_errback)
"""
agents_01 = []
agents_02 = []
for request in start_request_01():
    #(request.url)
    agent = downloader_01.fetch(request,spider)
    #agent.addCallback(request_callback)
    agents_01.append(agent)
for request in start_request_02():
    #(request.url)
    agent = downloader_02.fetch(request,spider)
    #agent.addCallback(request_callback)
    agents_02.append(agent)


#agent.addCallback(get_smzdm_datas)
#agent.addCallback(print_smzdm_result,url)
dd1 = defer.DeferredList(agents_01)
dd2 = defer.DeferredList(agents_02)
dd1.chainDeferred(dd2)
dd1.addBoth(lambda _: reactor.stop())

reactor.run()

