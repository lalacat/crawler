from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from twisted.web.http_headers import Headers
from zope.interface import implementer
from twisted.web.iweb import IBodyProducer
from twisted.internet.protocol import Protocol
from pprint import pformat
import json


class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)


headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})




def cbRequest(response):

    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    ''''''
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished
    #d = readBody(response)
    #d.addCallback(print_web)
    #return d

def print_web(result):
    #print(result)
    pass


@implementer(IBodyProducer)
class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, datas):
        '''
        :param bytes:
        :return:
        '''
        #if self.remaining:
        #display = json.load(datas)
        print(type(datas))
        display = datas.decode("utf-8")

        print('Some data received:')
        #print(display)


    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        self.finished.callback(None)

url = 'https://www.smzdm.com/homepage/json_more?p='
contextFactory = WebClientContextFactory()
agent = Agent(reactor, contextFactory)



#    d.addCallback(lambda ignored: reactor.stop())

result = list()
for i in range(1):
    i = str(i)
    u = url + i
    d = agent.request(b"GET", url.encode("utf-8"))
    #print(u)
    d.addCallback(cbRequest)
    result.append(d)

dd = defer.DeferredList(result)
dd.addBoth(lambda _: reactor.stop())
reactor.run()