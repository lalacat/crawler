from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import time
from queue import Queue




class Request(object):
    def __init__(self,url,parse):
        self.url = url
        self.parse = parse


class HttpResponse(object):

    def __init__(self,context,request):
        self.content = context
        self.request = request
        self.url = request.url
        self.text = request.parse(context,self.url)

class Scheduler(object):
    """
    任务调度器
    """
    def __init__(self):
        self.q = Queue()

    def open(self):
        pass

    def next_request(self):
        try:
            req = self.q.get(block=False)

        except Exception as e:
            req = None
        return req

    def enqueue_request(self,req):
        self.q.put(req)

    def size(self):
        return self.q.qsize()


class ExecutionEngine(object):
    """
    引擎：所有调度
    """
    def __init__(self):
        self._close = None
        self.scheduler = None

        #self.max = 5
        #self.crawlling = []

    def get_response_callback(content, request):
        print("get_response_callback")
        web_response = HttpResponse(content, request)

    def _next_request(self,name):
        print(name+':'+"next_request"+": 1")
        print(str(self.Q.qsize())+": 2")
        try:
            if self.Q.qsize() == 0 :
                print("task end")
                self.close.callback(None)
                return

            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            req = self.Q.get(block=0)
            d = getPage(req.url.encode('utf-8'))
            d.addCallback(self.get_response_callback,req)
            d.addCallback(lambda _:reactor.callLater(0,self.next_request,name))

        except Exception as e:
            print(e)

    @defer.inlineCallbacks
    def open_spider(self,start_requests):
        self.scheduler = Scheduler()
        yield self.scheduler.open()
        while True:
            try:
                req = next(start_requests)
            except StopIteration as e:
                break
            self.scheduler.enqueue_request(req)
        reactor.callLater(0,self._next_request)

    @defer.inlineCallbacks
    def start(self):
        self._close = defer.Deferred()
        yield self._close