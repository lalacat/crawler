from twisted.internet.ssl import ClientContextFactory
from twisted.python.log import err
from twisted.web.client import ProxyAgent
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint,SSL4ClientEndpoint

def display(response,url):
    print("Received response: %s"%url)
    print(response)
class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self,hostname, port):
        return ClientContextFactory.getContext(self)


contextFactory = WebClientContextFactory()

host = "149.28.192.96"
port = 527
def main():
    # endpoint = SSL4ClientEndpoint(reactor,host, port,contextFactory)
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 443)
    agent = ProxyAgent(endpoint)
    d = agent.request(b"GET", b"https://baidu.com/")
    d.addCallback(display,host)
    d.addErrback(err)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    main()