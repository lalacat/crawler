from spider.lianjia_spider_01 import LJSpider
from test.framework.core.crawler import Crawler
from test.framework.downloads import Downloader
from test.framework.setting import Setting
from test.framework.https.request import Request
from twisted.internet import reactor

import logging
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)

url = 'https://sh.lianjia.com/ershoufang/pg1'
headers = {
    'User-Agent':['Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/69.0.3497.81'
                  'Safari/537.36'],
    'content-type':['application/json']
}


def request_callback(content):
    print("request_and_response callback")
    print(type(content.body))
    print(content)
    print(content.body)
    return content.body


def request_errback(content):
    print("request_and_response errback")
    print(content[1])
    return content

def agent_print(content):
    print("agent_print")
    print(type(content))
    print(content)

request = Request(url=url,callback=request_callback,method='get',
                  headers=headers,errback=request_errback,meta={"download_timeout":2})

settings = Setting()
crawler = Crawler(LJSpider,settings)
spider = crawler._create_spider()
downloader = Downloader(crawler)

"""
httphandler = HTTPDownloadHandler(settings)
agent = httphandler.download_request(request,spider)
agent.addCallback(agent_print)
agent.addErrback(request_errback)
"""
agent = downloader.fetch(request,spider)
agent.addCallback(request_callback)
agent.addBoth(lambda _: reactor.stop())

reactor.run()

