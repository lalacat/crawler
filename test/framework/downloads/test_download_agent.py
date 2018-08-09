from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from twisted.web.iweb import IBodyProducer,UNKNOWN_LENGTH
from twisted.web._newclient import Response
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol

from urllib.parse import urldefrag
from zope.interface import implementer
import time,json,logging
from pprint import pformat
from test.framework.request.parse_url import to_bytes

logger = logging.getLogger(__name__)

class DownloaderClientContextFactory(ClientContextFactory):

    def getContext(self,host=None,port=None):
        print('getContext',host,port)
        return ClientContextFactory.getContext(self)


class DownloadAgent(object):
    _Agent = Agent

    def __init__(self,contextFactory=None, connectTimeout= 10, bindAddress=None,
                 pool=None,maxsize=0,warnsize=0,fail_on_dataloss=True):
        self._contextFactory = contextFactory
        self._connectTimeout = connectTimeout
        self._bindAddress = bindAddress
        self._pool = pool
        self._transferdata = None
        self._maxsize = maxsize # 规定最大的下载信息，防止下载的网页内容过大，占资源
        self._warnsize = warnsize# 给下载的网页设置一个警戒线
        self._fail_on_dataloss = fail_on_dataloss

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

        if request.body:
            bodyproducer = _RequestBodyProducer(request.body)
        elif method == b'POST':
            bodyproducer = _RequestBodyProducer(b'')
        else :
            bodyproducer = None
        start_time = time()

        d = agent.request(method,
              to_bytes(url),
              headers,
              bodyproducer)
        d.addCallback(self._cb_latency,request,start_time)
        d.addCallback(self._cbRequest)

    def _cb_latency(self,result,request, start_time):
        """记录延迟时间"""
        request.meta['download_latency'] = time() - start_time
        return result
    def _cbRequest(self,transferdata,request):
        '''
        print('Response _transport', response._transport)
        print('Response version:', response.version)
        print('Response code:', response.code)
        print('Response phrase:', response.phrase)
        print('Response phrase:', response._bodyBuffer)
        print('Response headers:')
        print(pformat(list(response.headers)))
        '''
        # 如果返回的response的Headers中包含了Content-Length，返回一个具体的数值
        # 如果Headers中不包含的话就是UNKNOWN_LENGTH
        if transferdata.length == 0:
            print("length: ", transferdata.length)

        #若meta中不存的'download_maxsize'这个值的话，会自动赋上默认值self._maxsize
        maxsize = request.meta.get('download_maxsize',self._maxsize)
        warnsize = request.meta.get('download_warnsize',self._warnsize)
        expected_size = transferdata.length if transferdata.length is not UNKNOWN_LENGTH else -1
        fail_on_dataloss = request.meta.get('download_fail_on_dataloss', self._fail_on_dataloss)

        #x and y布尔"与" - 如果 x 为 False，x and y 返回 False，否则它返回 y 的计算值。
        if maxsize and expected_size > maxsize :
            error_msg = ("%(url)s 网页的大小(%(size)s)已经超过可容许下载的最大值(%(maxsize)s).")
            error_args = {'url': request.url,"size":expected_size,'maxsize':maxsize}

            logger.error(error_msg,error_args)
            #twisted.protocols.tls.TLSMemoryBIOProtocol 的方法
            transferdata._transport._producer.loseConnection()

        def _cancel(_):
            transferdata._transport._producer.abortConnection()

        d = defer.Deferred(_cancel)
        transferdata.deliverBody()
        return d

@implementer(IBodyProducer)
class _RequestBodyProducer(object):

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


@implementer(IBodyProducer)
class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        #用来保存传输的数据，当数据完整后可以使用json转换为python对象
        self.result = bytes()
        self.num = 0

    def dataReceived(self, datas):
        '''
        直接传输的数据datas为bytes类型的，不加解码转化为str类型是带有转义符号'\':(\'\\u5929\\u732b\\u7cbe\\u9009\')
        datas进行了decode("utf-8")解码后，数据变成了('\u5929\u732b\u7cbe\u9009'),此时解码后的数据类型是str
        因为传输的datas并不是一次性传输完的，所以不能直接使用json转换，而是当数据全部传输完毕后，使用json.loads()
        这时候就不涉及到转码和转义字符的问题了。
        '''
        self.num += 1

        self.result += datas

    def connectionLost(self, reason):
        print('Finished receiving body:', reason.getErrorMessage())
        r = json.loads(self.result)
        #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
        #body传输到下一个函数中去
        self.finished.callback(r)

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
