from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import time

@inlineCallbacks
def crawl(*args,**kwargs):
    print("delay")
    d = begin()

    yield d
    yield finish('finish')

@inlineCallbacks
def begin(*args,**kwargs):
    print("begin")
    yield start('start')


def timedelay(num):
    print("休眠 :%d s"%num)
    for i in range(num,0,-1):
        print("倒计时：%d" %i)
        time.sleep(1)

def start(text):
    print(text)
    timedelay(5)

    returnValue("aaa")

def finish(text):
    print(text)
    returnValue("bbb")


def fun_print(text):
    print(text)
    return "ccc"

def fun_stop(text):
    print(text)
    try:
        reactor.stop()
    except Exception as e :
        print(e)
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

    for i in range(2):
        d = job("inner job ",i)
        d.addCallback(inner_fun,i)
        ts.append(d)
    dd = DeferredList(ts)
    return dd


def inner_fun(content,i):
    print("inner callback",content+str(i))
    return None


def _cb_timeout(result,d):
    if d.active():
        print("cancel")
        d.cancel()
        return result

if __name__ == "__main__":
    start = time.clock()

    ts = list()

    for i in range(2):
        d = job("outer job ",i)
        d.addCallback(outer_fun,i)
        ts.append(d)


    dd = DeferredList(ts)
    d= reactor.callLater(5,dd.cancel)
    dd.addBoth(_cb_timeout,d)
    dd.addCallback(lambda _:reactor.stop())


    reactor.run()

    end = time.clock()
    print("运行时间%3.2f" % (end - start))