from test.framework.test_import.spiderloader import SpiderLoader
from test.framework.crawler import Crawler,CrawlerRunner,CrawlerProcess,_get_spider_loader
from test.framework.record_live_instances import print_live_refs
from twisted.internet.defer import DeferredList
from twisted.internet import reactor
from test.framework.setting import Setting
import time


s = Setting()

cp = CrawlerProcess()
for name, module in cp.spider_loder._spiders.items():
    print(module)
    cp.crawl(module)

cp.start()