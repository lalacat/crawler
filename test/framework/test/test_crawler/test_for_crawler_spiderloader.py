from test.framework.core.crawler import Crawler,_get_spider_loader
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
from test.framework.setting import Setting
s = Setting()
cls = _get_spider_loader(s)

_active = set()
for name, module in cls._spiders.items():
    crawler = Crawler(module,s)
    #spider = crawler._create_spider()
    d = crawler.crawl()
    _active.add(d)


dd = DeferredList(_active)
if dd.called:
    print("have called")

#dd.addCallback(lambda _ :reactor.callLater(5,crawler.stop))
#dd.addCallback(crawler.stop)
dd.addBoth(lambda _:reactor.stop())


reactor.run()