from twisted.internet.defer import inlineCallbacks, Deferred, returnValue, DeferredList
from twisted.internet import reactor
from twisted.web.client import getPage


@inlineCallbacks
def my_callbacks(content):

    print ('first callback')

    returnValue((yield fun_test(content)))


def fun_test(content):
    print(content)
    for i in range(10):
        yield str(i)+":"+"test"

def fun_print(content):
    print(type(content))
    print(content)
    return content

def end_fun(content):
    print("end_content",content)
    try:
        reactor.stop()
    except Exception as e:
        print(e)

d = getPage(b"https://www.smzdm.com")
d.addCallback(my_callbacks)
d.addCallback(fun_print)
#d.addCallback(end_fun)

dd = DeferredList([d,])
dd.addBoth(end_fun)
reactor.run()

