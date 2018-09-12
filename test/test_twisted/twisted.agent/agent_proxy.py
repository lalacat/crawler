from twisted.python.log import err
from twisted.web.client import ProxyAgent
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

def display(response):
    print("Received response")
    print(response)

def main():
    endpoint = TCP4ClientEndpoint(reactor, "45.63.87.141", 3128)
    agent = ProxyAgent(endpoint)
    d = agent.request(b"GET", b"https://www.smzdm.com")
    d.addCallbacks(display, err)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    main()