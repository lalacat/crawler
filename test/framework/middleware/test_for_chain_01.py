from twisted.internet import reactor,defer
from twisted.web.client import getPage
from queue import Queue
from test.public_api.web import MongoDb
from urllib.parse import quote
from test.framework.test_import.import_spider import Spider
import time,logging
logger = logging.getLogger(__name__)



class SpiderMiddlewareManager(object):
    def __init__(self):
        super(SpiderMiddlewareManager, self).__init__()

    def process_start_requests(self, start_requests, spider):
        logger.info("process_start_requests")
        return process_chain({},start_requests, spider)

def process_chain(callbacks, input, *a, **kw):
    print("""Return a Deferred built by chaining the given callbacks""")
    d = defer.Deferred()
    for x in callbacks:
        print(x)
        d.addCallback(x, *a, **kw)
    print(d.callbacks)
    d.callback(input)
    return d

web_list = ["https://www.smzdm.com/homepage/json_more?p=1",
            "https://www.smzdm.com/homepage/json_more?p=2",
            "https://www.smzdm.com/homepage/json_more?p=3"]


sm = SpiderMiddlewareManager()
s = Spider(projectName="test")
d = sm.process_start_requests(iter(web_list),s)
print(d)

'''
@defer.inlineCallbacks
def test_fun():
    wi = iter(web_list)
    yield process_chain(wi,spider)



d = defer.Deferred()
d.addCallback(web_list[0])
d.addCallback(web_list[1])
d.addCallback(web_list[2])
print(d.callbacks)
try:
    dd = defer.DeferredList([d,])
except Exception as e :
    print(e)
dd.addBoth(lambda _:reactor.stop())
reactor.run()

'''