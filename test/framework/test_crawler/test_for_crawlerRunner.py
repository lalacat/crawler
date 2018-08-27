from test.framework.objectimport.spiderloader import SpiderLoader
from test.framework.crawler import Crawler,_get_spider_loader,CrawlerRunner
from test.framework.record_live_instances import print_live_refs
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
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