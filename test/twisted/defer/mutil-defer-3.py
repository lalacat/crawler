from twisted.internet.defer import Deferred ,returnValue ,inlineCallbacks ,DeferredList
from twisted.internet import reactor
from twisted.web.client import getPage


def outer_print(content):
    print("outer_callback",content)
    return 1


def inner_print(content):
    print("innner_callback",content)
    return 2

u2 = 'http://httpbin.org/get'

def inner_defer(content):
    # 返回的inner_defer的类型是defer类型，但是outer_defer的content是inner_defer的callback即inner_callback-innerprint的返回值

    print("child_defer",content)

    d = getPage(b"http://httpbin.org/get")
    d.addCallback(inner_print)

    return d
'''
当inner_defer的defer执行完后，会回到outer_defer继续执行

'''
outer_d = getPage(b'https://www.baidu.com')
outer_d.addCallback(outer_print)
outer_d.addCallback(inner_defer)
outer_d.addCallback(outer_print)
outer_d.addCallback(lambda _:reactor.stop())
reactor.run()
