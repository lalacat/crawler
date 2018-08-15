from twisted.internet.defer import Deferred,returnValue,inlineCallbacks,DeferredList
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.client import Agent, readBody
from twisted.internet.ssl import ClientContextFactory




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
    #d.addCallback(get_smzdm_datas)
    #d.addCallback(print_smzdm_result,url)
    return d


url = 'https://www.smzdm.com/homepage/json_more?p='
contextFactory = WebClientContextFactory()


class Requset(object):
    def __init__(self, url, parse):
        print("requset-->", url)
        self.url = url
        self.parse = parse


class HttpResponse(object):
    def __init__(self, content, request):
        self.content = content
        self.request = request
        self.url = request.url
        self.text = str(content, encoding="utf-8")


class Spider(object):
    name = "smzdm"

    def __init__(self,agent):
        self.agent = agent
        self.Flag = True
    def start_requests(self):
        start_url = ["https://www.baidu.com", "https://www.bing.com", ]
        for url in start_url:
            yield Requset(url, self.parse)

    def parse(self, response):
        print("---------response--------->", response)
        a = self.read_child_web(response,"d1")
        #a.callback(None)
        d2= self.agent.request(b'GET',b'http://httpbin.org/get')

        return d2

    def finish(self,content):
        print("finish")
        self.Flag = False

    def read_child_web(self,content,name):
        print('read_child_web',name)

        d = readBody(content)
        d.addCallback(self.print_child_web)
        return d

    def print_child_web(self,content):
        print("print_child_web:",content)
        #print(content)
        return

import queue

Q = queue.Queue()


class Engine(object):
    crawlling = list()
    max = 5

    def __ini__(self):
        self._close = None

    def get_response_callback(self, content, request):
        #print("get_response_callback")
        self.crawlling.remove(request)
        #print(rep.content)

        result = request.parse(content)
        result.addCallback(self.inner_print)
        return result


    def _next_request(self,spider):
        print("spider name:",spider.name)
        print('----->request_and_response', Q.qsize())
        if Q.qsize() == 0 and len(self.crawlling) == 0:
            self._close.callback(None)
            return

        while len(self.crawlling) < self.max:
            try:
                req = Q.get(block=False)
                self.crawlling.append(req)
                # getPage返回的是一个defer对象
                d = spider.agent.request(b"GET", req.url.encode("utf-8"))
                print("d",d)

                # 当页面下载完之后，会立即调用回调函数get_response_callback
                d.addCallback(self.outer_print)
                d.addCallback(self.get_response_callback, req)
                d.addCallback(self.outer_print)
                d.addCallback(lambda _:reactor.callLater(0,self._next_request,spider))
            except Exception as e:
                print("Exception",e)
                break
               #print(e)

    def outer_print(self,content):
        print("outer_callback", content)
        return 1

    def inner_print(self,content):
        print("innner_callback", content)
        return 2

    @inlineCallbacks
    def crwal(self, spider):
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration as e:
                break

        #print(Q.qsize())
        reactor.callLater(0, self._next_request,spider)

        self._close = Deferred()
        yield self._close

def end():
    print("end")
    reactor.stop()

agent = Agent(reactor, contextFactory)

spider = Spider(agent)
#_active = set()
engine = Engine()
d = engine.crwal(spider)

#_active.add(d)

dd = DeferredList([d,])
dd.addCallback(lambda _:reactor.stop())

reactor.run()
