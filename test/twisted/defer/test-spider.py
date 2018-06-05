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

class Spider(object):
    name = "smzdm"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def start_requests(self):
        #start_url = ["https://www.baidu.com","https://www.bing.com",]
        start_url = list()
        for i in range(1):
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

def parse_test(context):
    print('parse_test',context)
    i = 1
    for i in range(10):
        time.sleep(1)
        i += 1
    return i


@defer.inlineCallbacks
def parse_web(context):
    test = "parse_test"
    d = defer.Deferred()
    d.addCallback(parse_test)
    reactor.callLater(0,d.callback,test)
    yield d

class HttpRespose(object):
    def __init__(self,context,request):
        self.content = context
        self.request = request
        self.url = request.url
        self.text = parse_test(context)
        print(self.text)



def get_response_callback(content,request):
    web_response = HttpRespose(content,request)
    request.parse.callback(content)
    print("content:",content)


spider = Spider()
import queue
Q = queue.Queue()
start_request = iter(spider.start_requests())
print(start_request)
while True:
    try:
        request = next(start_request)
        #print(request)
        Q.put(request)
    except StopIteration as e:
        break


print(Q.qsize())
#如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
while Q.qsize() != 0:
    req = Q.get(block=0)
    d = getPage(req.url.encode('utf-8'))
    d.addCallback(get_response_callback)


