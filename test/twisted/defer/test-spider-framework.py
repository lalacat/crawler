from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import time
from queue import Queue

class Spider1(object):
    name = "task1"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        self.q = Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(5):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        #self. num = start_url.__len__()
        #print(start_url.count())

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print('parse1', url)
        i = 1
        for i in range(1):
            # time.sleep(1)
            i += 1
            # print(i)
        return i


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
        print("open")
        pass

    def next_request(self):
        try:
            req = self.q.get(block=False)

        except Exception as e:
            req = None
        return req

    def enqueue_request(self,req):
        self.q.put(req)

    def qsize(self):
        return self.q.qsize()


class ExecutionEngine(object):
    """
    引擎：所有调度
    """
    def __init__(self):
        print("引擎初始化")
        self._close = None
        self.scheduler = None
        #self.max = 5
        #self.crawlling = []

    def get_response_callback(self,content, request):
        print("get_response_callback")
        web_response = HttpResponse(content, request)

    def print_web(self,content):
        print("get content")

    def _next_request(self,name):
        print(name+':'+"next_request"+": 1")
        print(str(self.scheduler.qsize())+": 2")
        try:
            if self.scheduler.qsize() == 0 :
                print("task end")
                self._close.callback(None)
                return

            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            req = self.scheduler.next_request()
            print(req.url)
            d = getPage(req.url.encode('utf-8'))
            #d.addCallback(self.print_web)
            d.addCallback(self.get_response_callback,req)
            d.addCallback(lambda _:reactor.callLater(0,self._next_request,name))

        except Exception as e:
            print(e)

    @defer.inlineCallbacks
    def open_spider(self,spider):

        self.scheduler = Scheduler()
        yield self.scheduler.open()
        start_requests = iter(spider.start_requests())
        while True:
            print("读取网站")
            try:
                req = next(start_requests)
                print(req)
            except StopIteration as e:
                print("读取网站失败")
                break
            self.scheduler.enqueue_request(req)
        reactor.callLater(0,self._next_request,spider.name)

    @defer.inlineCallbacks
    def start(self):
        self._close = defer.Deferred()
        yield self._close


class Crawler(object):
    """
    用户封装调度器以及引擎的...
    """
    def _create_engine(self):
        return ExecutionEngine()

    def _create_spider(self,spider_cls_path):
        """
        :param spider_cls_path:  spider.chouti.ChoutiSpider
        :return:
        """
        module_path,cls_name = spider_cls_path.rsplit('.',maxsplit=1)
        import importlib
        m = importlib.import_module(module_path)
        cls = getattr(m,cls_name)
        return cls()

    @defer.inlineCallbacks
    def crawl(self):
        engine = self._create_engine()
        #spider = self._create_spider(spider_cls_path)
        spider = Spider1()
        print(spider)

        yield engine.open_spider(spider)
        yield engine.start()



if __name__ == "__main__":
    crawl = Crawler()
    d = crawl.crawl()
    dd = defer.DeferredList([d,])
    dd.addBoth(lambda _:reactor.stop())
    reactor.run()