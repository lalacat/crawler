from __future__ import print_function

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web._newclient import Response




agent = Agent(reactor)

d = agent.request(
    b'GET',
    b'https://www.baidu.com',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    None)

def cbResponse(ignored):
    print('Response received')
    print(type(ignored))
    print(ignored._bodyDataReceived)

d.addCallback(cbResponse)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()