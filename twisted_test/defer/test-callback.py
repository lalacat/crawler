from twisted.internet import defer,reactor
import time
'''
测试callback（）方法的用法
实现不同defer数据的传送

'''

class Request(object):
    def __init__(self,url,parse):
        self.url = url
        self.parse = parse

    def get_print(self):
        print("callback")
        self.parse.callback(self.url)


class HtttpRespose(object):
    def __init__(self,content,request):
        self.content = content
        self.requset = request
        self.url = request.url


def parse_test(context):
    print('parse_test')
    i = 1
    for i in range(10):
        time.sleep(1)
        i += 1
    return i


@defer.inlineCallbacks
def parse_web(context):
    test = "parse_test"
    d = defer.Deferred()
    d.addCallback(parse_test)
    reactor.callLater(0,d.callback,context)
    yield d

def print1(data):
    print("print1")
    print(type(data))
    print(data)
    return "return from print1"

def print2(data):
    print("print2")
    print(data)
    return "return from print2"


if __name__ == "__main__":
    d1 = defer.Deferred()
    d2 = defer.Deferred()
    d1.addCallback(print1)
    d1.addCallback(print2)
    r = Request("request_and_response",d1)
    rep = HtttpRespose("content",r)
    result = r.parse.callback(rep)
    print(type(result))



