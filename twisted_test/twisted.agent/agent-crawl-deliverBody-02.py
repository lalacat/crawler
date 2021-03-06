from twisted.web.client import Agent,readBody
from twisted.internet import reactor,defer
from twisted.internet.ssl import ClientContextFactory
from twisted.web.http_headers import Headers
from zope.interface import implementer
from twisted.web.iweb import IBodyProducer
from twisted.internet.protocol import Protocol
from pprint import pformat
from twisted.web._newclient import Response
import json
import time
from test.public_api.web import get_smzdm_datas,print_smzdm_result,end_crawl
headers = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})


class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def cbRequest(response,u,i):
    '''
    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)


    print("i", i)
    if i == "0":
        print("loseConnection")
        error_msg = ("%(url)s 网页的大小(%(size)s)已经超过可容许下载的最大值(%(maxsize)s).")
        error_args = {'url':u , "size": "10m", 'maxsize': "1020m"}

        print("从(%(request_and_response)s)收取到的信息容量(%(bytes)s) bytes 超过了下载信息的"
                         "警戒值(%(warnsize)s) bytes " % {
                'request_and_response' : u,
                'bytes' : 100,
                'warnsize' : 90
            })

        response._transport._producer.loseConnection()
        raise defer.CancelledError(error_msg % error_args)
    '''
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished,i,response))
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
    def __init__(self, finished,i,response):
        self.finished = finished
        #用来保存传输的数据，当数据完整后可以使用json转换为python对象
        self.result = bytes()
        self.num = i
        self.time = 0
        self.response = response

    def dataReceived(self, datas):
        '''
        直接传输的数据datas为bytes类型的，不加解码转化为str类型是带有转义符号'\':(\'\\u5929\\u732b\\u7cbe\\u9009\')
        datas进行了decode("utf-8")解码后，数据变成了('\u5929\u732b\u7cbe\u9009'),此时解码后的数据类型是str
        因为传输的datas并不是一次性传输完的，所以不能直接使用json转换，而是当数据全部传输完毕后，使用json.loads()
        这时候就不涉及到转码和转义字符的问题了。
        '''
        self.time += 1
        ''' 
        if self.time == 3:
            print("lose Connection")
            temp =self.response._transport._producer
            print(type(temp))
            self.response._transport._producer.loseConnection()
        '''
        self.result += datas

    def connectionLost(self, reason):
        print('Finished receiving body:', self.num,reason.getErrorMessage())
        #print(len(self.result))
        print(" %s 数据有丢失，如果要处理这个错误的话，在默认设置中"
              "将DOWNLOAD_FAIL_ON_DATALOSS = False"
              %self.response.request.absoluteURI.decode())


        r = json.loads(self.result)
        #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
        #body传输到下一个函数中去
        self.finished.callback(r)


url = 'https://www.smzdm.com/homepage/json_more?p='
contextFactory = WebClientContextFactory()



agent = Agent(reactor, contextFactory)
result = list()
t1 = time.time()
for i in range(3):
    i = str(i)
    u = url + i
    print(u)
    d = agent.request(b"GET", u.encode("utf-8"))
    d.addCallback(cbRequest,u,i)
    d.addErrback(lambda result: print(result))

    #d.addCallback(get_smzdm_datas)
    #d.addCallback(print_smzdm_result,u)
    result.append(d)

dd = defer.DeferredList(result)
dd.addBoth(end_crawl,t1)
reactor.run()