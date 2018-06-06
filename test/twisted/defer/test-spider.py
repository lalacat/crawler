from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer
import time

class Request(object):
    def __init__(self,url,parse):
        self.url = url
        self.parse = parse
       # self.parse.addCallback(self.get_print)

    def get_print(self):
        print("callback")
        self.parse.callback(self.url)


class Spider1(object):
    name = "task1"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def start_requests(self):
        start_url = list()

        for i in range(5):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            print(url)
            yield Request(url,self.parse)

    def parse(self,response):
        print("---------response--------->",response)
        d = defer.Deferred()
        #return d
        #yield Request('http://www.cnblogs.com',callback=self.parse)


class Spider2(object):
    name = "task2"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def start_requests(self):
        start_url = list()
        for i in range(5,10):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            print(url)
            yield Request(url,self.parse)

    def parse(self,response):
        print("---------response--------->",response)
        d = defer.Deferred()

def parse_test(context,url):
    print('parse_test',url)
    i = 1
    for i in range(1):
        time.sleep(1)
        i += 1
        #print(i)
    return i


@defer.inlineCallbacks
def parse_web(context,url):
    test = "parse_test"
    d = defer.Deferred()
    d.addCallback(parse_test,url)
    yield d

class HttpRespose(object):
    def __init__(self,context,request):
        self.content = context
        self.request = request
        self.url = request.url
        self.text = parse_test(context,self.url)
        #print(self.text)



def get_response_callback(content,request):
    print("get_response_callback")

    web_response = HttpRespose(content,request)
    #print("content:",content)


def next_request(name):
    print(name)
    print(Q.qsize())
    if Q.qsize() == 0 :
        print("task end")
        pass

    while Q.qsize() != 0:
        # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
        req = Q.get(block=0)
        print(req)
        print(req.url)
        d = getPage(req.url.encode('utf-8'))
        d.addCallback(get_response_callback,req)


spider1 = Spider1()
spider2 = Spider2()
task_list = list()



#@defer.inlineCallbacks
def crawl(spider):
    print(spider.name)
    start_request = iter(spider.start_requests())
    while True:
        try:
            request = next(start_request)
            #print(request)
            Q.put(request)
        except StopIteration as e:
            break

    reactor.callLater(0,next_request,spider.name)
    #close = defer.Deferred()
    #yield close



import queue
Q = queue.Queue()
#task1 = crawl(spider1)
crawl(spider1)
#task2 = crawl(spider2)


#task_list.append(task1)
#task_list.append(task2)

#dd = defer.DeferredList(task_list)


#print(Q.qsize())


#dd.addCallback(lambda _:reactor.stop())
reactor.run()


