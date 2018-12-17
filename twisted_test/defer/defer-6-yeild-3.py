from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import requests
from lxml import etree

from twisted.web.client import getPage


header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

urls = ["https://www.smzdm.com/p2/",
       "https://www.smzdm.com/p4/" ,
        "https://www.smzdm.com/p5/"]



def request(url):
    result = requests.get(url,headers=header)
    return result

def response(content):
    print(content)


@defer.inlineCallbacks
def task():
    print("start job")
    d = Deferred()
    reactor.callWhenRunning(d.callback,request("https://www.smzdm.com/p4/"))
    d.addCallback(response)
    print("job end")
    #d.addCallback(response)
    yield d


li = []
for i in range(2):
    d = task()
    li.append(d)
dd = defer.DeferredList(li)
dd.addBoth(lambda _:reactor.stop())
reactor.run()