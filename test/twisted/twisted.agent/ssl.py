import sys

from zope.interface import implementer

from twisted.internet.task import react
from twisted.internet.ssl import optionsForClientTLS

from twisted.web.iweb import IPolicyForHTTPS
from twisted.web.client import Agent, ResponseFailed, BrowserLikePolicyForHTTPS

@implementer(IPolicyForHTTPS)
class OneHostnameWorkaroundPolicy(object):
    def __init__(self):
        self._normalPolicy = BrowserLikePolicyForHTTPS()
    def creatorForNetloc(self, hostname, port):
        print(hostname)
        print(port)
        return self._normalPolicy.creatorForNetloc(hostname, port)

@react
def main(reactor):
    agent = Agent(reactor, OneHostnameWorkaroundPolicy())
    requested = agent.request(b"GET", sys.argv[1].encode("ascii"))
    def gotResponse(response):
        print(response.code)
    def noResponse(failure):
        failure.trap(ResponseFailed)
        print(failure.value.reasons[0].getTraceback())
    return requested.addCallbacks(gotResponse, noResponse)