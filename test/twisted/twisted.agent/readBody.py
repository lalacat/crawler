from __future__ import print_function



from twisted.internet.task import react
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.internet.ssl import optionsForClientTLS
from twisted.web.iweb import IPolicyForHTTPS
from twisted.web.client import Agent, ResponseFailed, BrowserLikePolicyForHTTPS
from zope.interface import implementer


headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})
def cbRequest(response):
    '''

    print('Response version:', response.version)
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))

    '''

    d = readBody(response)
    d.addCallback(cbBody)
    return d

def cbBody(body):
    print('Response body:')
    print(body)


@implementer(IPolicyForHTTPS)
class OneHostnameWorkaroundPolicy(object):
    def __init__(self):
        self._normalPolicy = BrowserLikePolicyForHTTPS()
    def creatorForNetloc(self, hostname, port):
        if hostname == b"wrong.host.badssl.com":
            hostname = b"badssl.com"
        return self._normalPolicy.creatorForNetloc(hostname, port)


def main(reactor, url="https://www.smzdm.com"):
    agent = Agent(reactor)
    #agent = Agent(reactor)
    d = agent.request(
        b'GET',
        url.encode("utf-8"),
        headers,
        None)
    d.addCallback(cbRequest)
    return d

react(main)
