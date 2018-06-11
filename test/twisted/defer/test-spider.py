from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import time,queue


class Request(object):
    def __init__(self,url,parse):
        self.url = url
        self.parse = parse


class Spider1(object):
    name = "task1"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        self.q = queue.Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(5):
            i = str(i)
            u = self.url + i
            start_url.append(u)

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

class Spider2(object):
    name = "task2"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        self.q = queue.Queue()

    def start_requests(self):
        start_url = list()
        for i in range(5,10):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            #print(url)
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print('parse2', url)
        i = 1
        for i in range(1):
            # time.sleep(1)
            i += 1
            # print(i)
        return i



class Spider3(object):
    name = "task3"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        self.q = queue.Queue()

    def start_requests(self):
        start_url = list()
        for i in range(10,15):
            i = str(i)
            u = self.url + i
            start_url.append(u)


        for url in start_url:
            #print(url)
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print('parse3', url)
        i = 1
        for i in range(1):
            # time.sleep(1)
            i += 1
            # print(i)
        return i



class Spider4(object):
    name = "task4"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        self.q = queue.Queue()

    def start_requests(self):
        start_url = list()
        for i in range(15,20):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print('parse4', url)
        i = 1
        for i in range(1):
            # time.sleep(1)
            i += 1
            # print(i)
        return i



'''
def parse_test(context,url):
    print('parse_test',url)
    i = 1
    for i in range(1):
        #time.sleep(1)
        i += 1
        #print(i)
    return i
    
@defer.inlineCallbacks
    def parse_web(context,url):
        test = "parse_test"
        d = defer.Deferred()
        d.addCallback(parse_test,url)
        yield d

'''


class HttpRespose(object):

    def __init__(self,context,request):
        self.content = context
        self.request = request
        self.url = request.url
        self.text = request.parse(context,self.url)


def get_response_callback(content,request):
    print("get_response_callback")
    web_response = HttpRespose(content,request)


class engine(object):

    def __init__(self):
        self.close = None
        self.Q = None

    @defer.inlineCallbacks
    def crawl(self,spider,Q):
        self.Q = Q
        #print(spider.name)
        start_request = iter(spider.start_requests())
        while True:
            try:
                request = next(start_request)
                Q.put(request)
            except StopIteration as e:
                break

        reactor.callLater(0,self.next_request,spider.name)
        self.close = defer.Deferred()
        yield self.close

    def next_request(self,name):
        print(name+':'+"next_request"+": 1")
        print(str(self.Q.qsize())+": 2")
        try:
            if self.Q.qsize() == 0 :
                print("task end")
                self.close.callback(None)
                return

           # while Q.qsize() != 0:
            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            req = self.Q.get(block=0)
            d = getPage(req.url.encode('utf-8'))
            d.addCallback(get_response_callback,req)
            d.addCallback(lambda _:reactor.callLater(0,self.next_request,name))

        except Exception as e :
            print(e)


if __name__ == "__main"():
    spider1 = Spider1()
    spider2 = Spider2()
    spider3 = Spider3()
    spider4 = Spider4()
    task_list = list()

    engine1 = engine()
    engine2 = engine()
    engine3 = engine()
    engine4 = engine()

    task1 = engine1.crawl(spider1,spider1.q)
    task2 = engine2.crawl(spider2,spider2.q)
    task3 = engine3.crawl(spider3,spider3.q)
    task4 = engine4.crawl(spider4,spider4.q)

    task_list.append(task1)
    task_list.append(task2)
    task_list.append(task3)
    task_list.append(task4)

    dd = defer.DeferredList(task_list)
    dd.addCallback(lambda _:reactor.stop())
    reactor.run()


