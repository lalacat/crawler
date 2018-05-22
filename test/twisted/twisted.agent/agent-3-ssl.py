from twisted.python.log import err
from twisted.web.client import Agent
from twisted.internet import reactor
from twisted.internet.ssl import ClientContextFactory
import traceback
class WebClientContextFactory(ClientContextFactory):
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def display(response):
    print("Received response")
    print(response.body)
def display_err(response):
    print(response)
    traceback.print_stack()

def main():
    contextFactory = WebClientContextFactory()
    agent = Agent(reactor, contextFactory)
    d = agent.request(b"GET", b"https://www.smzdm.com/")

    d.addCallbacks(display, display_err)
    d.addCallback(lambda ignored: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    main()