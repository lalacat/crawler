from test.framework.crawler import Crawler, _get_spider_loader
from test.framework.setting import Setting
from test.framework.test_import.loadobject import load_object


class Slot(object):

    def __init__(self,concurrency,delay,randomize_delay):
        pass


class Downloader(object):
    def __init__(self,crawler):
        self.settings = crawler.settings
        self.handler = load_object(self.settings["DOWNLOAD_HANDLER"])



class DownloaderMiddlewareManager(object):

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

s = Setting()
cls = _get_spider_loader(s)

for name, module in cls._spiders.items():
    print(name)
    crawler = Crawler(module,s)
    d = Downloader(crawler)

