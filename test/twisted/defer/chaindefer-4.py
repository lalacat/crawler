from twisted.internet.defer import Deferred,returnValue,inlineCallbacks,DeferredList
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.web.client import Agent, readBody
from twisted.internet.ssl import ClientContextFactory







url = 'https://www.smzdm.com/homepage/json_more?p='

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

    def __init__(self):
        self.Flag = True
    def start_requests(self):
        start_url = ["https://www.baidu.com", "https://www.bing.com", ]
        for url in start_url:
            yield Requset(url, self.parse)

    def parse(self, response):
        print("---------response--------->")
        #a.callback(None)
        d2 = getPage(b"http://httpbin.org/get")
        return d2

    def finish(self,content):
        print("finish")
        self.Flag = False


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
        print('----->request', Q.qsize())
        if Q.qsize() == 0 and len(self.crawlling) == 0:
            self._close.callback(None)
            return

        while len(self.crawlling) < self.max:
            try:
                req = Q.get(block=False)
                self.crawlling.append(req)
                # getPage返回的是一个defer对象
                d = getPage(req.url.encode("utf-8"))
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
        print("outer_callback")
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


spider = Spider()
#_active = set()
engine = Engine()
d = engine.crwal(spider)

#_active.add(d)

dd = DeferredList([d,])
#dd.addCallback(lambda _:reactor.stop())

reactor.run()
