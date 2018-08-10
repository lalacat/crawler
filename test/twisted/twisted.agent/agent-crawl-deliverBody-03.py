from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from twisted.web.http_headers import Headers
from zope.interface import implementer
from twisted.web.iweb import IBodyProducer
from twisted.internet.protocol import Protocol
from pprint import pformat
from io import BytesIO

import json
import time,logging
from test.public_api.web import get_smzdm_datas,print_smzdm_result,end_crawl

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)


headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})


class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def cbRequest(response,url):

    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    ''''''
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished,url))
    finished.addErrback(lambda a:print("error",a))
    return finished
    #d = readBody(response)
    #d.addCallback(print_web)
    #return d

def print_web(result):
    print("finish")
    print(type(result))
    print(result)

    pass
    return



@implementer(IBodyProducer)
class BeginningPrinter(Protocol):
    def __init__(self, finished,url):
        self.finished = finished
        #用来保存传输的数据，当数据完整后可以使用json转换为python对象
        self._bodybuf = BytesIO()
        self._bytes_received = 0
        self._maxsize = 1000
        self._request = url


    def dataReceived(self, datas):
        '''
        直接传输的数据datas为bytes类型的，不加解码转化为str类型是带有转义符号'\':(\'\\u5929\\u732b\\u7cbe\\u9009\')
        datas进行了decode("utf-8")解码后，数据变成了('\u5929\u732b\u7cbe\u9009'),此时解码后的数据类型是str
        因为传输的datas并不是一次性传输完的，所以不能直接使用json转换，而是当数据全部传输完毕后，使用json.loads()
        这时候就不涉及到转码和转义字符的问题了。
        '''
        if self.finished.called:
            return
        if self._bytes_received >= 1000:
            print("cancel")
            #self.finished(None)

        if self._maxsize and self._bytes_received > self._maxsize:
            logging.info("从(%(request)s)收取到的信息容量(%(bytes)s) bytes 超过了下载信息的"
                         "最大值(%(maxsize)s) bytes " % {
                'request' : self._request,
                'bytes' : self._bytes_received,
                'maxsize' : self._maxsize
            })
            self.finished.cancel()
        self._bytes_received += len(datas)
        self._bodybuf.write(datas)

    def connectionLost(self, reason):
        print('Finished receiving body:',self._bytes_received, reason.getErrorMessage())
        result = self._bodybuf.getvalue()
        r = json.loads(result)
        #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
        #body传输到下一个函数中去
        self.finished.callback(r)


url = 'https://www.smzdm.com/homepage/json_more?p='
contextFactory = WebClientContextFactory()



agent = Agent(reactor, contextFactory)
result = list()
t1 = time.time()
for i in range(1):
    i = str(i)
    u = url + i
    print(u)
    d = agent.request(b"GET", u.encode("utf-8"))
    d.addCallback(cbRequest,u)
    d.addCallback(get_smzdm_datas)
    d.addCallback(print_smzdm_result,u)
    result.append(d)

dd = defer.DeferredList(result)
dd.addBoth(end_crawl,t1)
reactor.run()