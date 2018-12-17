from twisted.internet.defer import Deferred,returnValue,inlineCallbacks,DeferredList,CancelledError
from twisted.internet import reactor
from twisted.web.client import getPage

def print1(d):
    print('print1 one',d)
    raise ValueError('test')
    return d

def error1(d):
    print('error1 one')
    print(d)
    return d

def print2(d):
    print('print2 two')
    print(d)
    return d

def error2(d):
    print('error2 two')
    print(d)
    return d

def reportCancel(fail, which):
    fail.trap(CancelledError)
    print('cancelled', which)

def print_fun(d):
    print("print_fun",d)
    return d

url = 'https://www.smzdm.com/homepage/json_more?p='
d1 = Deferred()
d1.addCallback(print1)
d1.addErrback(error1)
d2 = Deferred().addBoth(print_fun)
d2.addCallbacks(print2,error2)

d1.chainDeferred(d2)
reactor.callLater(2,d1.callback,"hey")
reactor.run()
