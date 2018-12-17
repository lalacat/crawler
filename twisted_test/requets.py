import requests
import time

def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))

def request_web():
    try:
        res = requests.get("https://www.baidu.com",timeout=10)
    except Exception as e:
        print(e)
        return
    print(res)

from twisted.internet import reactor,task

reactor.callWhenRunning(hello,"lala")

reactor.callLater(1,request_web)
reactor.callLater(3,hello,"lala")

reactor.run()