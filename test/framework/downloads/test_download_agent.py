from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from urllib.parse import urldefrag
from twisted.internet.defer import Deferred
from pprint import pformat
from twisted.web.http_headers import Headers
from test.framework.request.parse_url import to_bytes

from twisted.web._newclient import Response

class DownloaderClientContextFactory(ClientContextFactory):

    def getContext(self,host=None,port=None):
        print('getContext',host,port)
        return ClientContextFactory.getContext(self)


class DownloadAgent(object):
    _Agent = Agent

    def __init__(self,contextFactory=None, connectTimeout= 10, bindAddress=None,
                 pool=None):
        self._contextFactory = contextFactory
        self._connectTimeout = connectTimeout
        self._bindAddress = bindAddress
        self._pool = pool

    def _getAgent(self,timeout):

        return self._Agent(reactor,contextFactory=self._contextFactory,
                           connectTimeout=timeout,
                           bindAddress=self._bindAddress,
                           pool=self._pool)

    def download_request(self,request):
        timeout = request.meta.get('download_timeout') or self._connectTimeout
        agent = self._getAgent(request,timeout)
        #url格式如下：protocol :// hostname[:port] / path / [;parameters][?query]#fragment
        # urldefrag去掉fragment
        url = urldefrag(request.url)[0]
        method = to_bytes(request.method)
        headers = request.headers

'''

contextFactory = DownloaderClientContextFactory()
headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})
agent = Agent(reactor, contextFactory)
d = agent.request(b'GET',
              b'https://smzdm.com',
              headers=headers,
              )
def cbRequest(response):
    print('Response _transport',response._transport)
    print('Response version:', response.version)
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    print('Response phrase:',response._bodyBuffer)
    print('Response headers:')
    print(pformat(list(response.headers)))

    d = readBody(response)
    return d
d.addCallback(cbRequest)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()
'''
