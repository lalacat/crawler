from test.framework.core.crawler import _get_spider_loader,CrawlerRunner
from twisted.internet.defer import DeferredList
from twisted.internet import reactor

'''
cls = _get_spider_loader()

_active = set()
cr = CrawlerRunner()
module = cls._spiders["task1"]
for name, module in cls._spiders.items():
    print(module)
    cr.crawl(module)

print(cr._active)

dd = DeferredList(cr._active)

#dd.addCallback(lambda _ :reactor.callLater(5,crawler.stop))
#dd.addCallback(crawler.stop)
dd.addBoth(lambda _:reactor.stop())


reactor.run()
'''

def generator_fun():
    for i in range(10):
        yield i

d = generator_fun()
print(type(d))
flag = True
while True:
    try:
        print(d.__next__())
    except StopIteration:
        flag = False
        print("载入完毕")
        break