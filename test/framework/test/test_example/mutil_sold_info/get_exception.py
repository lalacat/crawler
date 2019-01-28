import OpenSSL
from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.error import ConnectionLost, ConnectionDone
from twisted.python import failure
import time,random
from twisted.internet.interfaces import IReactorTime
from twisted.web._newclient import ResponseNeverReceived


def job(text,id):

    def test_01():
        raise ResponseNeverReceived('test_01')

    def test_02():
        raise TimeoutError('test_02')

    def test_03():
        raise ConnectionLost('test_03')

    def test_04():
        raise ConnectionDone('test_04')

    def test_05():
        raise  OpenSSL.SSL.Error('test_05')

    return task.deferLater(reactor, 2, test_05)


def outer_fun(content):

    print("out_fun",content)
    return "outer"

def err_fun(exception):
    failure = exception.value
    temp = dict()
    temp['failure'] = str(failure)
    # print(type(temp['failure']))

    # print(failure)
    # print(temp)
    if isinstance(failure,ResponseNeverReceived):
        print(failure)
        print(temp)

    elif isinstance(failure,TimeoutError):
        # if isinstance(failure,BaseException):
        #     print(failure.args[0])
        print(failure)
        print(temp)
    elif isinstance(failure,ConnectionLost):
        # if isinstance(failure,BaseException):
        #     print(failure.args[0])
        print(failure)
        print(temp)
    elif isinstance(failure, ConnectionDone):
        # if isinstance(failure,BaseException):
        #     print(failure.args[0])
        print(failure)
        print(temp)
    elif isinstance(failure, OpenSSL.SSL.Error):
        # if isinstance(failure,BaseException):
        #     print(failure.args[0])
        print(failure)
        print(temp)

    return None


def print_fun(content):
    print("print callback", content)
    return None

d = job("test",1)
d.addCallbacks(outer_fun,err_fun)

d.addBoth(lambda _:reactor.stop())

reactor.run()