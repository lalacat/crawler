from twisted.internet import reactor,defer
from twisted.web.client import getPage
import requests

def print_web(content,num):
    print("print_web:%d"%num)
    print(content)

def print_child_web(content,num):
    print("print_child_web:%d"%num)

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


#@defer.inlineCallbacks
def get_page(url):
    d = getPage(url.encode("utf-8"))
    #d.addCallback(get_child_web)
    d.addCallback(print_web,1)
    d.addCallback(lambda _:reactor.callLater(0,get_child,b"https://www.smzdm.com/"))

    #yield d

if __name__ == '__main__':

    reactor.callLater(0, get_page, "https://www.baidu.com/")
    reactor.run()