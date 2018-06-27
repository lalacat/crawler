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
d2 = Deferred().addCallback(cancel1)
d3 = Deferred().addCallback(cancel2)

d1.chainDeferred(d2)
d1.chainDeferred(d3)

d1.callback('hey')