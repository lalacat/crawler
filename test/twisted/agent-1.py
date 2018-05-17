from twisted.internet import reactor,defer
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.ssl import ClientContextFactory


class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        print(hostname)
        return ClientContextFactory.getContext(self)

headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})

#headers=Headers({'User-Agent':['Twisted WebBot'],
#                 'Content-Type':['text/x-greeting']})

def print_web(result):
    print("read web")
    print(result)


contextFactory = WebClientContextFactory()
agent = Agent(reactor, contextFactory)
url = b"https://www.smzdm.com"
#url =
d = agent.request('GET',url,headers=headers)
d.addCallback(print_web)
d.addBoth(lambda _: reactor.stop())
reactor.run()