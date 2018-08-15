from twisted.web.client import HTTPClientFactory
from twisted.internet import reactor
from test.framework.request_and_response.parse_url import _parsed
from test.framework.downloads.download_agent import HTTPDownloadHandler
from test.framework.setting import Setting
from test.framework.request_and_response import Request
from spider.spider1 import Spider1

url = 'https://www.smzdm.com/homepage/json_more?p=1'
headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]}


def request_callback(content):
    print("request_and_response callback")
    print(content)


def request_errback(content):
    print("request_and_response errback")
    print(content)

if callable(request_callback):
    print("callable")

request = Request(url=url,callback=request_callback,method='get',headers=headers,errback=request_errback)

settings = Setting()

spider = Spider1()
httphandler = HTTPDownloadHandler(settings)


