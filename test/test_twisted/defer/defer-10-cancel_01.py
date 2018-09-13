from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import time

from twisted.python.log import err


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
from twisted.internet import reactor,defer,task
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
import time,random


def job(text,id):
    def _cancel(_):
        print("job cancel")
    d = defer.Deferred(_cancel)
    print(text + str(id))
    d.callback(random.randint(1, 5))
    return d


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
    print("inner callback",content,str(i))
    return content


def _cb_timeout(result,d):
    print("called!!!")
    if d.active():
        print("reactor,cancel")
        d.cancel()
        return "active finish"
    return "finish"

def test_fun(id):

    d = job("test: ",id)
    print(d)
    print(type(d))
    #d.addCallback(outer_fun,1)
    c = reactor.callLater(1,d.cancel)
    d.addCallback(_cb_timeout,c)
    return d

def print_fun(result):
    print(result)
    return "stop"

def stop_fun(result):
    print(result)
    try:
        reactor.stop()
    except Exception as e :
        print(e)

if __name__ == "__main__":
    start = time.clock()

    try:
        d = test_fun(1)
        d.addCallback(print_fun)
        d.addBoth(stop_fun)
        reactor.run()
    except Exception as e :
        print(e)
