from twisted.internet import reactor,defer
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.ssl import ClientContextFactory
from twisted.web.iweb import IAgent
class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        print(hostname)
        return ClientContextFactory.getContext(self)

headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})

headers=Headers({'User-Agent':['Twisted WebBot'],
                 'Content-Type':['text/x-greeting']})

def print_web(result):
    print("read web")
    print(result)

@defer.inlineCallbacks
def request_web():
    agent = Agent(reactor)
    url = b'http://www.baidu.com'
    print(type(url))
    try:
        result = yield agent.request('GET', url,headers, None)
    except Exception as e:
        print(e)
        return

reactor.callWhenRunning(print_web, 'yudahai')

reactor.callLater(1, request_web)

reactor.callLater(3, print_web, 'yuyue')
reactor.callLater(3,reactor.stop)

reactor.run()