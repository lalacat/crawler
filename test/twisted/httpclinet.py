import time
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, task, defer

def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))

@defer.inlineCallbacks
def request_web():
    agent = Agent(reactor)
    try:
        result = yield agent.request('GET', 'http://www.baidu.com', Headers({'User-Agent': ['Twisted Web Client Example']}), None)
    except Exception as e:
        print(e)
        return
    print(result)


reactor.callWhenRunning(hello, 'yudahai')

reactor.callLater(1, request_web)

reactor.callLater(3, hello, 'yuyue')

reactor.run()