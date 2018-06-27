from twisted.internet.defer import Deferred,returnValue,inlineCallbacks,DeferredList
from twisted.internet import reactor
from twisted.web.client import getPage




class Requset(object):
    def __init__(self, url, callback):
        print("requset-->", url)
        self.url = url
        self.callback = callback


class HttpResponse(object):
    def __init__(self, content, request):
        self.content = content
        self.request = request
        self.url = request.url
        self.text = str(content, encoding="utf-8")


class Spider(object):
    name = "smzdm"

    def __init__(self):
        self.dd = Deferred()

    def start_requests(self):
        start_url = ["https://www.baidu.com", "https://www.bing.com", ]
        for url in start_url:
            yield Requset(url, self.parse)

    def parse(self, response):
        #print("---------response--------->", response)
        self.dd.addCallback(self.print_child_web)

    @inlineCallbacks
    def second_defer(self):
        print('second callback')
        #yield getPage(b"http://httpbin.org/get")




    def print_child_web(self,content):
        print("print_child_web:")
        print(content)
        return


import queue

Q = queue.Queue()


class Engine(object):
    crawlling = list()
    max = 5

    def __ini__(self):
        self._close = None

    def get_response_callback(self, content, request):
        self.crawlling.remove(request)
        rep = HttpResponse(content, request)
        print(rep.content)

        result = request.callback(rep)

        return "child defer"

        import types
        if isinstance(result, types.GeneratorType):
            for rep in result:
                # print(rep)
                Q.put(rep)

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
                d = getPage(req.url.encode('utf-8'))
                # 当页面下载完之后，会立即调用回调函数get_response_callback
                d.addCallback(self.get_response_callback, req)
                if spider.dd is not None :
                    print("add chainDeferred")
                    d.chainDeferred(spider.dd)

                d.addCallback(lambda _:reactor.callLater(0,self._next_request,spider))
            except Exception as e:
                print(e)
                return "Exception defer"

    @inlineCallbacks
    def crwal(self, spider):
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration as e:
                break

        print(Q.qsize())
        reactor.callLater(0, self._next_request,spider)

        self._close = Deferred()
        yield self._close


spider = Spider()
_active = set()
engine = Engine()
d = engine.crwal(spider)

_active.add(d)

dd = DeferredList(_active)
dd.addBoth(lambda _: reactor.stop())
reactor.run()
