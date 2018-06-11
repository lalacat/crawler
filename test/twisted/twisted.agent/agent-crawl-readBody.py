from twisted.web.client import Agent, readBody
from twisted.internet import reactor, defer
from twisted.internet.ssl import ClientContextFactory
from twisted.web.http_headers import Headers
import time
from test.public_api.web import get_need_datas, print_result, end_crawl

headers = Headers({'User-Agent': ['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                   'content-type': ["application/json"]})


class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)


def cbRequest(response,url):
    '''
    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    '''

    d = readBody(response)
    d.addCallback(get_need_datas)
    d.addCallback(print_result,url)
    return d


url = 'https://www.smzdm.com/homepage/json_more?p='
contextFactory = WebClientContextFactory()

agent = Agent(reactor, contextFactory)
result = list()
t1 = time.time()
for i in range(50):
    i = str(i)
    u = url + i
    d = agent.request(b"GET", u.encode("utf-8"))
    d.addCallback(cbRequest,u)
    #d.addCallback(get_need_datas)
    #d.addCallback(print_result, u)
    result.append(d)

dd = defer.DeferredList(result)
dd.addBoth(end_crawl, t1)
reactor.run()