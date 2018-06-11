from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from test.public_api.web import get_need_datas,print_result
import json,time
import pymongo

from test.public_api.web import get_need_datas,print_result,end_crawl

url = 'https://www.smzdm.com/homepage/json_more?p='
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "Twisted_Database"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "getPage_Collection"
db_coll = db[COLLECTION ]


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