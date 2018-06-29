from twisted.internet import reactor,defer
from twisted.internet.defer import returnValue,Deferred,DeferredList
from twisted.web.client import getPage
import requests

def print_web(content):
    #print("print_web:%s"%num)
    print(content)

def print_child_web(content):
    print("print_child_web:")
    print(content)

def get_child_web(content):
    print("child web")

    try:
        reactor.callLater(0,get_child,"https://www.baidu.com/")
    except Exception as e:
        print(e)

@defer.inlineCallbacks
def get_child():
    print("get_child")

    yield getPage(b"http://httpbin.org/get")



@defer.inlineCallbacks
def get_page(url):
    d = getPage(url.encode("utf-8"))
    d.addCallback(print_child)
    #d.addCallback(lambda _:reactor.stop())

    yield d




def print_child(content):
    print("print_child")

    d = second_defer()
    d.addCallback(print_web)
    #d.result
    #d.addCallback(print_web)

    d.addCallback(lambda _: reactor.stop())

@defer.inlineCallbacks
def second_defer():
    print('first callback')
    result = yield getPage(b"http://httpbin.org/get")
    returnValue(result)


if __name__ == '__main__':
    d = defer.Deferred()

    d = get_page("https://www.baidu.com/")
    dd = DeferredList([d,])

    #dd.addBoth(lambda _: reactor.stop())
    reactor.run()