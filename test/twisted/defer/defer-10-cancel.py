from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import time

def response(_):
    print(_)
    for i in range(3):
        print(i)
        time.sleep(1)
    return "bbb"

def time_wasted_wrapper(job_id):
    def request():
        result = 'time-wasted job '+str(job_id)+' done!'
        return result
    print('begin time-wasted job '+str(job_id))
    # 返回一个deferred对象，真实情况下，这里可能是一个直接返回deferred对象的函数，也可能是一个正常阻塞函数，但是你可以用
    # deferToThread来获得一个deferred对象
    return task.deferLater(reactor, 2, request)
def fun_print(_):
    print(_)
    return "ccc"



d = time_wasted_wrapper(1)
d.addCallback(response)
timeout = reactor.callLater(1,d.cancel)
d.addCallback(fun_print)
d.addCallback(lambda _:reactor.stop())
reactor.run()