from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, Protocol, connectionDone


class SimpleProtocol(Protocol):
    rev_data = ''

    def dataReceived(self, data):
        print(data)
        self.rev_data += data

    def connectionLost(self, reason=connectionDone):
        self.factory.finished(self.rev_data)

class SimpleClientFactory(ClientFactory):
    protocol = SimpleProtocol

    def __init__(self,deferred):
       self.deferred = deferred

    def finished(self,data):
        if self.deferred is not None:
            d,self.deferred = self.deferred,None
            d.callback(data)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d,self.deferred = self.deferred,None
            d.errback(reason)

def print_data(_):
    print('print_data')
    print(_)
    reactor.stop()

def print_err(_):
    print(_)
    reactor.stop()

try:
    d = Deferred()
    factory = SimpleClientFactory(d)
    reactor.connectTCP("149.28.192.96", 5527, factory)
    d.addCallback(print_data)
    reactor.run()
except Exception as e :
    print(e)