from test.framework.crawler import Crawler
from test.framework.test_import.loadobject import load_object


class Slot(object):

    def __init__(self,concurrency,delay,randomize_delay):
        pass


class Downloader(object):
    def __init__(self,crawler):
        self.settings = crawler.settings
        self.handler = load_object(self.settings["DOWNLOAD_HANDLERS"])

c = Crawler()