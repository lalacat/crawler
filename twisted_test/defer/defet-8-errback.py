from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor
from twisted.python import failure
import time,random
from twisted.internet.interfaces import IReactorTime
def job(text,id):

    print(text + str(id))
    def request(id):
        try:
            a = 2/id
            print(a)
            return "task Finish "
        except Exception as e :
             return failure.Failure("数字不能整除")
    return task.deferLater(reactor, 1, request,id)


def outer_fun(content):

    print("out_fun",content)
    return "outer"

def err_fun(content):

    print("err_fun",content)
    return "error"


def print_fun(content):
    print("print callback", content)
    return None

d = job("test",1)
#d.addCallbacks(outer_fun,err_fun)
#d.addTimeout(3,clock=None,onTimeoutCancel=None)
d.addCallback(lambda f:print("print",f))
d.addCallback(print_fun,print_fun)
d.addBoth(lambda _:reactor.stop())

reactor.run()