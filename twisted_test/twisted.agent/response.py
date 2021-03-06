from __future__ import print_function

from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers



headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})

class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):
        '''


        :param bytes:
        :return:
        '''
        if self.remaining:
            display = bytes[:self.remaining]
            print('Some data received:')
            print(display)
            self.remaining -= len(display)
            #print(bytes)

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        self.finished.callback(None)

agent = Agent(reactor)
d = agent.request(
    b'GET',
    b'https://www.smzdm.com')

def cbRequest(response):
   # print('Response version:', response.version)
    print('Response code:', response.code)
   # print('Response phrase:', response.phrase)
    #print('Response headers:')
   # print(pformat(list(response.headers.getAllRawHeaders())))
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished
d.addCallback(cbRequest)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()