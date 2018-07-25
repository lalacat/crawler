import time
from twisted.internet import reactor,defer
from twisted.internet import reactor,defer,task
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
import time,random
'''
callFromThread 的线程池是由 ：
tp = reactor.getThreadPool()和tp.adjustPoolsize(maxthreads）来决定大小
在由 reactor.run() 激发的主消息循环（main event loop）中执行，所以也就能被 reactor.stop() 终止执行。

callInThread 在 reactor 的一个私有线程池里工作的
reactor.suggestThreadPoolSize(15)
来设置该线程池的大小。默认最小是5个线程，最大10个
'''



def job(text,id):
    def timedelay(id,num):
        print("%d休眠 :%d s"%(id,num))
        for i in range(num,0,-1):
            print("倒计时：%d" %i)
            time.sleep(1)
        if id == 6:
            reactor.callInThread(pause, text + str(id))
        return "task Finish "




    return task.deferLater(reactor, 1, timedelay,id,1)


def outer_fun(content,id):
    print(content+str(id))
    ts = list()

    for i in range(5):
        d = job("inner job ",i)
        #d.addCallback(inner_fun,i)
        ts.append(d)
    dd = DeferredList(ts)
    return dd


def inner_fun(content,i):
    print("inner callback",content+str(i))
    return None

def finish(content,i):
    print("callback ",content+str(i))
    return None

def pause(context):
    print(context,"pause")

if __name__ == "__main__":
    start = time.clock()

    tp = reactor.getThreadPool()
    tp.adjustPoolsize(maxthreads=5)

    ts = list()

    for i in range(12):
        d = job("outer job ",i)
        d.addCallback(finish,i)
        ts.append(d)


    dd = DeferredList(ts)
    dd.addCallback(lambda _:reactor.stop())




    reactor.run(installSignalHandlers=False)

    end = time.clock()
    print("运行时间%3.2f" % (end - start))




