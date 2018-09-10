import time

from twisted.internet import task, defer, reactor

from test.framework.https.request import Request


def parallel(iterable, count, callable, *args, **named):
    """
    实现同时控制处理，多个defer的功能
    Cooperator是实现Cooperative task的，这是一个能够迭代的iterator，能够提供一个最基本的实现work。当处于yield状态的时候，
    Cooperator能够决定下个执行的task是哪个，如果yield，是一个deferred，work会一直等到这个deffered链执行完。
    当Cooperator有多个task的时候，它能够分配这些work在这些tasks中来回切换，相当于实现并行操作。
    cooperate返回是一个CooperativeTask，它的作用是启动一个给定的iterator作为一个长期执行的cooperative task
    这个task能够pause,resumed和waited on
    coiterate是添加一个iterator到正在运行的Cooperator的iterator list中去，等同于cooperate，但是返回的是一个Deferred
    """
    coop = task.Cooperator()
    work = (callable(elem, *args, **named) for elem in iterable)
    print(type(work))
    for i in work:
        print("i",i)
    return defer.DeferredList([coop.coiterate(work) for _ in range(count)])

def print_fun(content):
    t = time.clock()
    print("print_fun",content,t)
    return content
def start_requests():
    start_url = list()

    for i in range(3):
        i = "start_request"+str(i)
        start_url.append(i)

    for url in start_url:
        yield url


def print_result(content,start):
    end = time.clock()
    print(type(content))
    print(end-start)
    for i in content:
        #print(dir(i)
        pass

    print(dir(content[0]))
    print(content[0].__next__())
    for i in content[0]:
        print("i",i)
    return "test"
start  = time.clock()
dd = parallel(start_requests(),3,print_fun)
dd.addCallback(lambda r: [x[1] for x in r])
#dd.addCallback(print_result,start)
#dd.addCallback(lambda f:print(f))
dd.addCallback(lambda _:reactor.stop())
reactor.run()

print(time.clock())
print(time.time())
