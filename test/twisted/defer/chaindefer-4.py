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
        self.url = "http://httpbin.org/get"
    def start_requests(self):
        start_url = ["https://www.baidu.com", "https://www.bing.com", "https://www.sogou.com/"]
        for url in start_url:
            yield Requset(url, self.parse)

    def parse(self, response):
        print("---------response--------->")

        d2 = getPage(b"http://httpbin.org/get")
        d2.addCallback(self.inner_callback)
        try:
            print("str:", d2.result.value)
        except Exception as e :
            print(e)
        return d2

    def inner_callback(self,content):
        print("Spider_inner:",content)
        return "callback %s" %self.url

import queue

Q = queue.Queue()


class Engine(object):
    crawlling = list()
    max = 5

    def __ini__(self):
        self._close = None

    def get_response_callback(self, content, request):

        result = request.parse(content)

        result.addCallback(self.engine_inner)
        print("get_response_callback end")
        return result


    def _next_request(self,spider):
        print(str(Q.qsize()),str(len(self.crawlling)))

        if Q.qsize() == 0 and len(self.crawlling) == 0:
            self._close.callback(None)
            return None
        print("spider name:",spider.name)

        while Q.qsize() > 0 :
            try:
                req = Q.get(block=False)
                # getPage返回的是一个defer对象
                d = getPage(req.url.encode("utf-8"))

                # 当页面下载完之后，会立即调用回调函数get_response_callback
                d.addCallback(self.engine_outer,req.url,1)
                d.addCallback(self.get_response_callback, req)
                d.addCallback(self.engine_outer,req.url,2)
                self.crawlling.append(req.url)
                d.addCallback(self.finish,req.url)

                d.addCallback(lambda _:reactor.callLater(0,self._next_request,spider))
            except Exception as e:
                print("Exception",e)
                break
            print("循环结束")




    def engine_outer(self,content,url,num):
        print("engine_outer： 返回%s的内容 : %d"%(url,num))
        return "engine_outer %s" %url

    def engine_inner(self,content):
        print("engine_inner", content)
        return "engine_inner"
    def finish(self,content,url):
        print(content)
        self.crawlling.remove(url)
        return None


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
dd.addCallback(lambda _:reactor.stop())

reactor.run()
