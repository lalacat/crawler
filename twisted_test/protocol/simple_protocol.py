from twisted.internet import reactor
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

    def __init__(self,callback,errback):
        self.callback = callback
        self.errback = errback

    def finished(self,data):
        self.callback(data)

    def clientConnectionFailed(self, connector, reason):
        self.errback(reason)

def print_data(_):
    print(_)
    reactor.stop()

def print_err(_):
    print(_)
    reactor.stop()

try:
    factory = SimpleClientFactory(print_data,print_err)
    reactor.connectTCP("149.28.192.96", 5527, factory)
    reactor.run()
except Exception as e :
    print(e)