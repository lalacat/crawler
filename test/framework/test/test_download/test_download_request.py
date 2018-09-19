from twisted.internet import reactor

from spider.spider1 import Spider1
from test.framework.core.crawler import Crawler
from test.framework.downloads import Downloader
from test.framework.https.request import Request
from test.framework.setting import Setting
url = 'https://www.smzdm.com/homepage/json_more?p=1'
headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]}

def request_callback(content):
    print("request_and_response callback")
    print(content)


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
crawler = Crawler(Spider1,settings)
spider = crawler._create_spider()
downloader = Downloader(crawler)
try:
    dtd = downloader._download(request,spider)
    dtd.addBoth(request_callback)
except Exception as e :
    print(e)

dtd.addBoth(lambda _: reactor.stop())

reactor.run()