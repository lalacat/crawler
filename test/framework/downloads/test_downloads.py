class HttpsDownloadHandler(object):
    def __init__(self,settings=None):
        pass

from twisted.web.client import HTTPClientFactory
from twisted.internet import reactor
from test.framework.request_and_response.parse_url import _parsed

def getPage(url, contextFactory=None, *args, **kwargs):
    """Download a web page as a string.

    Download a page. Return a deferred, which will callback with a
    page (as a string) or errback with a description of the error.

    See HTTPClientFactory to see what extra args can be passed.
    """
    scheme, host, port, path = _parsed(url)
    print(host,port)
    factory = HTTPClientFactory(url.encode('utf-8'), *args, **kwargs)
    if scheme == 'https':
        from twisted.internet import ssl
        if contextFactory is None:
            contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(host, port, factory, contextFactory)
    else:
        reactor.connectTCP(host, port, factory)
    return factory.deferred

def print_fun(content):
    print(content)
d = getPage("https://www.smzdm.com/homepage/json_more?p=1")
print(type(d))
d.addCallback(print_fun)

reactor.run()