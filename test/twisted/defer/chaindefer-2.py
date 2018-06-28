from twisted.internet.defer import Deferred,returnValue,inlineCallbacks,DeferredList,CancelledError
from twisted.internet import reactor
from twisted.web.client import getPage

def cancel1(d):
    print('cancel one')
    print(d)


def cancel2(d):
    print('cancel two')
    print(d)


def reportCancel(fail, which):
    fail.trap(CancelledError)
    print('cancelled', which)


d1 = Deferred()
d2 = getPage(b"http://httpbin.org/get")
d2.addCallbacks(cancel2,cancel2)
#d3 = Deferred().addCallback(cancel2)
d1.addCallback(cancel1)
d1.chainDeferred(d2)
#d1.chainDeferred(d3)
#print(d1.callbacks)
d1.callback('hey')
