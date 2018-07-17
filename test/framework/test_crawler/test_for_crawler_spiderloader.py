from test.framework.test_import.spiderloader import SpiderLoader
from test.framework.crawler import Crawler,_get_spider_loader
from test.framework.record_live_instances import print_live_refs
from twisted.internet.defer import DeferredList
cls = _get_spider_loader()

_active = set()
for name, module in cls._spiders.items():
    crawler = Crawler(module)
    #spider = crawler._create_spider()
    d = crawler.crwal()


dd = DeferredList(_active)
print(dd)