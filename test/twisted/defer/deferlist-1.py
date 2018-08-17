from twisted.web.client import getPage
from twisted.internet import reactor,defer,task
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
import time,random


def job(text,id):
    def request():
        #time.sleep(1)
        return "task Finish "

    print(text + str(id))

    return task.deferLater(reactor, random.randint(1,5), request)


def outer_fun(content,id):
    print(content+str(id))
    ts = list()

    for i in range(5):
        d = job("inner job ",i)
        d.addCallback(inner_fun,i)
        ts.append(d)
    dd = DeferredList(ts)
    return dd


def inner_fun(content,i):
    print("inner callback",content+str(i))
    return None


if __name__ == "__main__":
    start = time.clock()

    ts = list()

    for i in range(10):
        d = job("outer job ",i)
        d.addCallback(outer_fun,i)
        ts.append(d)


    dd = DeferredList(ts)
    dd.addCallback(lambda _:reactor.stop())


    reactor.run()

    end = time.clock()
    print("运行时间%3.2f" % (end - start))