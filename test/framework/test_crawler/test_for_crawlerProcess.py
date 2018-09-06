from test.framework.crawler import CrawlerProcess
from test.framework.setting import Setting

s = Setting()

cp = CrawlerProcess()
for name, module in cp.spider_loder._spiders.items():
    print(module)
    cp.crawl(module)

cp.start()
cp.stop()