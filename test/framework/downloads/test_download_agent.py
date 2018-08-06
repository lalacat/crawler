from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from twisted.internet.defer import Deferred
from pprint import pformat

class DownloaderClientContextFactory(ClientContextFactory):

    def getContext(self,host=None,port=None):
        print('getContext',host,port)
        return ClientContextFactory.getContext(self)

contextFactory = DownloaderClientContextFactory()
agent = Agent(reactor, contextFactory)
d = agent.request(b'GET',
              b'https://baidu.com',
              None,
              None
              )
def cbRequest(response):
    print('Response version:', response.version)
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))

    d = readBody(response)
    return d
d.addCallback(cbRequest)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()
