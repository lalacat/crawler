from twisted.python.log import err
from twisted.web.client import ProxyAgent
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint

def display(response,url):
    print("Received response: %s"%url)
    print(response)


urls = ["124.205.155.154","112.95.207.240","27.191.234.69","45.63.87.141"]
prots = [9090,8888,9999,3128]
def main():
    agents = []
    for url,prot in zip(urls,prots):
        endpoint = TCP4ClientEndpoint(reactor,url, prot)
        agent = ProxyAgent(endpoint)
        d = agent.request(b"GET", b"https://www.smzdm.com")
        d.addCallback(display,url)
        d.addErrback(err)
        agents.append(d)
    dd = defer.DeferredList(agents)
    dd.addCallback(lambda ignored: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    main()