from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer


def response(we):
    print(we)



@defer.inlineCallbacks
def task():
    url = "https://www.baidu.com"
    print(url)
    d1 = getPage(url.encode('utf-8'))
    d1.addCallback(response)
    yield d1
    ''' 
    url = "https://www.baidu.com"
    d2 = getPage(url.encode('utf-8'))
    d2.addCallback(response)
    #yield d2

    url = "https://www.baidu.com"
    d3 = getPage(url.encode('utf-8'))
    d3.addCallback(response)
    yield defer.Deferred()
    '''


def done(*args,**kwargs):
    reactor.stop()

li = []
for i in range(1):
    d = task()
    li.append(d)
#d = task()
#dd = defer.DeferredList([d,])
#dd.addBoth(done)

reactor.run()