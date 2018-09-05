
from twisted.internet.defer import Deferred ,returnValue ,inlineCallbacks ,DeferredList ,CancelledError
from twisted.internet import reactor
import twisted.internet.defer
from twisted.web.client import Agent,readBody
from twisted.internet.ssl import ClientContextFactory
from test.public_api.web import get_smzdm_datas, print_smzdm_result, end_crawl

from twisted.python import log

class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)


contextFactory = WebClientContextFactory()
agent = Agent(reactor, contextFactory)

u1 = 'https://www.baidu.com'
u2 = 'https://httpbin.org/get'


def print1(d):
    print('print1 one',d)
    return d

def print2(d):
    print('print2 two',d)


def print_child_web(content):
    print("child_web",content)
    return "print_child_web"

def chlid_defer(content):
    print("child_defer",content)

    d2 = agent.request(b"GET", u2.encode("utf-8"))
    d2.addCallback(cbRequest)
    return d2

def cbRequest(response):
    '''
    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    '''
    # 虽然返回的是d是一个defer类型的数据，但是在返回上一级addCallBack的函数中接收的content是d的callback方法中print_child_web的返回值
    d = readBody(response)
    d.addCallback(print_child_web)
    return d


d1 = agent.request(b"GET", u1.encode("utf-8"))
d1.addCallback(print1)
d1.addCallback(cbRequest)
d1.addCallback(print1)
d1.addCallback(chlid_defer)
d1.addCallback(print2)
d1.addCallback(lambda _:reactor.stop())

reactor.run()
#d2.callback('hey')
#d1.callback('jude')