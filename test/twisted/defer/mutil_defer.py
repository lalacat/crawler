from twisted.internet import reactor,defer
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


def get_child(url):
    print("get_child",url)

    d = getPage(url)

    d.addCallback(print_child_web)
    d.addCallback(lambda _:reactor.stop())
    d.callback("stop")


@defer.inlineCallbacks
def get_page(url):
    d = getPage(url.encode("utf-8"))
    d.addCallback(print_child)
    #d.addCallback(lambda _:reactor.stop())

    yield d


def print_child(content):
    print("print_child")

    d = second_defer(content)
    d.addCallback(print_web)
    #d.addCallback(lambda _: reactor.stop())
    #print(d)

@defer.inlineCallbacks
def second_defer(content):
    print('first callback')
    #yield getPage(b"http://httpbin.org/get")

    d = defer.Deferred()
    reactor.callLater(2, d.callback, 2)
    result = yield d # yielded deferreds will pause the generator
    print(result)
    defer.returnValue(result)

if __name__ == '__main__':
    d = get_page("https://www.baidu.com/")
    dd = defer.DeferredList([d,])
    dd.addBoth(lambda _: reactor.stop())
    reactor.run()