from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent, HTTPConnectionPool

class IgnoreBody(Protocol):
    def __init__(self, deferred):
        self.deferred = deferred

    def dataReceived(self, bytes):
        #print("get in ")
        pass

    def connectionLost(self, reason):
        self.deferred.callback("finish")


def cbRequest(response):
    print('Response code:', response.code)
    finished = Deferred()
    response.deliverBody(IgnoreBody(finished))
    return finished

pool = HTTPConnectionPool(reactor,persistent=True)
agent = Agent(reactor, pool=pool)

def requestGet(url):
    d = agent.request(b'GET', url.encode('utf-8'))
    d.addCallback(cbRequest)
    return d

def print_fun(clientprotocol,i):
    try:
        d = clientprotocol.request(i)
        d.addCallback(fun_print)
    except Exception as e :
        print(e)
    return d

def fun_print(con):
    print(con)
# Two requests to the same host:
d =  requestGet('http://www.baidu.com/')
d1 = requestGet("http://ping.chinaz.com/")
d2 = requestGet("http://tool.chinaz.com/sitespeed/")
d3 = requestGet("http://www.baidu.com/")
dd = DeferredList([d,d1,d2,d3])
def cbShutdown(ignored):
    for i in pool._connections.keys():
        #print(i)
        try:
            finsh = Deferred()
            d = pool.getConnection(i,finsh)
            #finsh.addCallback(print_fun)
            d.addCallback(print_fun,i)

        except Exception as e :
            print(e)
    #d = pool.getConnection("baidu",'com')
    #d.callback(cbRequest)
    #reactor.stop()
dd.addCallback(cbShutdown)

reactor.run()