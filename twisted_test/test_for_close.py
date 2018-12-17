from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import time


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

    def start_requests(self):
        start_url = ["https://www.baidu.com", "https://www.bing.com",
                     "https://www.baidu.com", "https://www.bing.com",
                     "https://www.baidu.com", "https://www.bing.com"]
        for url in start_url:
            yield Requset(url, self.parse)

    def parse(self, content):
        print("---------response--------->", content)
        time.sleep(3)
        return "response 已收到"


import queue

Q = queue.Queue()


class Engine(object):
    crawlling = list()
    max = 5

    def __ini__(self):
        self._close = None
        self._num = 0
    def get_response_callback(self, content, request):

        result = request.parse(request.url)
        return result


    def _next_request(self):
        #print('----->request_and_response', Q.qsize())
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
                d.addCallback(self.finish,req,self._num)
                d.addCallback(lambda _:reactor.callLater(0,self._next_request))

            except Exception as e:
                print(e)
                return

    def finish(self,content,req,num):
        print(content)
        self.crawlling.remove(req)
        if num == 3:
            self._close.callback(None)
        self._num += 1
        return "finish"



    @defer.inlineCallbacks
    def crwal(self, spider):
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration as e:
                break

        print(Q.qsize())
        reactor.callLater(0, self._next_request)

        self._close = defer.Deferred()
        yield self._close


spider = Spider()
_active = set()
engine = Engine()
d = engine.crwal(spider)

_active.add(d)

dd = defer.DeferredList(_active)
dd.addBoth(lambda _: reactor.stop())
reactor.run()