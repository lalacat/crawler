from test.framework.crawler import Crawler,_get_spider_loader
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
from test.framework.setting import Setting
s = Setting()
cls = _get_spider_loader(s)

_active = set()
for name, module in cls._spiders.items():
    print(name,module)
    crawler = Crawler(module,s)
    #spider = crawler._create_spider()
    d = crawler.crawl()
    _active.add(d)


dd = DeferredList(_active)

#dd.addCallback(lambda _ :reactor.callLater(5,crawler.stop))
#dd.addCallback(crawler.stop)
dd.addBoth(lambda _:reactor.stop())


reactor.run()