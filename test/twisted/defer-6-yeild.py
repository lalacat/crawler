from twisted.internet.defer import inlineCallbacks,Deferred,returnValue

from twisted.internet import reactor,defer


def loadRemoteData(callback):
    import time
    time.sleep(1)
    callback(1)


def loadRemoteData2(callback):
    import time
    time.sleep(1)
    callback(2)


@defer.inlineCallbacks
def getRemoteData():
    d1 = defer.Deferred()
    reactor.callInThread(loadRemoteData, d1.callback)
    r1 = yield d1

    d2 = defer.Deferred()
    reactor.callInThread(loadRemoteData2, d2.callback)
    r2 = yield d2

    returnValue(r1 + r2)


def getResult(v):
    print
    "result=", v


if __name__ == '__main__':
    d = getRemoteData()
    d.addCallback(getResult)

    reactor.callLater(4, reactor.stop);
    reactor.run()