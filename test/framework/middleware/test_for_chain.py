from twisted.internet import defer
from spider import spider1

def process_chain(callbacks, input, *a, **kw):
    """Return a Deferred built by chaining the given callbacks"""
    d = defer.Deferred()
    for x in callbacks:
        d.addCallback(x, *a, **kw)
    d.callback(input)
    return d


class MiddlewareManager(object):
    def _process_chain(self, methodname, obj, *args):
        return process_chain(self.methods[methodname], obj, *args)


class SpiderMiddlewareManager(MiddlewareManager):
    def process_start_requests(self, start_requests, spider):
        return self._process_chain('process_start_requests', start_requests, spider)

url = "https://www.smzdm.com/homepage/json_more?p="

def start_requests(url):
    start_url = list()

    for i in range(1):
        i = str(i)
        u = url + i
        start_url.append(u)

    for url in start_url:
        yield url

def fun () :
    sm = SpiderMiddlewareManager()
    sr = iter(start_requests(url))
    s = spider1()
    d = yield sm.process_start_requests(sr,s)

if __name__ == '__main__':
    fun()