from twisted.internet.defer import inlineCallbacks, Deferred, returnValue


@inlineCallbacks
def my_callbacks():
    from twisted.internet import reactor

    print ('first callback')
    result = yield 1 # yielded values that aren't deferred come right back

    print ('second callback got', result)
    d = Deferred()
    reactor.callLater(3, d.callback, "test value")
    #result = yield d # yielded deferreds will pause the generator
    yield d # yielded deferreds will pause the generator

    #print ('third callback got', result) # the result of the deferred
    #returnValue(result)


def fun_test(context):
    print(context)
    return context

from twisted.internet import reactor
d = my_callbacks()
print(type(d))
print(d)
d.addCallback(fun_test)
d.addCallback(lambda _:reactor.stop())
reactor.run()

