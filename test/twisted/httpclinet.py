import time
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, task, defer

headers=Headers({'User-Agent':['Twisted WebBot'],
                 'Content-Type':['text/x-greeting']})

def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))



@defer.inlineCallbacks
def request_web():
    agent = Agent(reactor)
    url = b'https://www.baidu.com'
    print(type(url))
    try:
        result = yield agent.request('GET', url,headers, None)

    except Exception as e:
        print(e)
        return
    print(result)


reactor.callWhenRunning(hello, 'yudahai')

reactor.callLater(1, request_web)

reactor.callLater(3, hello, 'yuyue')
reactor.callLater(3,reactor.stop)
reactor.run()