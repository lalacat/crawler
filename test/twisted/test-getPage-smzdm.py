from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
import json,time
from test.public_api.web import get_need_datas,print_result,end_crawl

url = 'https://www.smzdm.com/homepage/json_more?p='
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

@inlineCallbacks
def read_url(url):
    d = getPage(url.encode('utf-8'))
    d.addCallback(get_need_datas)
    d.addCallback(print_result,url)
    yield d


if __name__ == '__main__':
    t1 = time.time()
    result = list()
    for i in range(10):
        i = str(i)
        u = url + i
        d = read_url(u)
        result.append(d)

    dd = defer.DeferredList(result)
    dd.addBoth(end_crawl,t1)
    reactor.run()