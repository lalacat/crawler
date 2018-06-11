from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from test.public_api.web import get_need_datas,print_result
import json,time
import pymongo

from test.public_api.web import get_need_datas,print_result,end_crawl,MongoDb

url = 'https://www.smzdm.com/homepage/json_more?p='
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}




def insert_mongoDb(result,db_coll):
    if isinstance(result,list):
        for post in result:
            try:
                db_coll.insert_one(post)
            except Exception as e :
                print(e)
        print("MongoDb update Finish")

    return result

@inlineCallbacks
def read_url(url,db_coll):
    d = getPage(url.encode('utf-8'))
    d.addCallback(get_need_datas)
    d.addCallback(insert_mongoDb,db_coll)
    d.addCallback(print_result,url)
    yield d


if __name__ == '__main__':
    t1 = time.time()

    '''
    
    
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"

    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)

    # 连接到数据库myDatabase
    DATABASE = "Twisted_Database"
    db = client[DATABASE]

    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "getPage_Collection"
    db_coll = db[COLLECTION]
    '''

    db = MongoDb("127.0.0.1:27017","Twisted_Database","getPage_Collection")
    db._connectDb()
    db_coll = db._getCollection()

    result = list()

    for i in range(10):
        i = str(i)
        u = url + i
        d = read_url(u,db_coll)
        result.append(d)

    dd = defer.DeferredList(result)
    dd.addBoth(end_crawl,t1)
    reactor.run()