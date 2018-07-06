from bs4 import BeautifulSoup
from twisted.python import failure
class BaseSpider(object):
    pass
class Request(object):
    def __init__(self, url, parse):
        self.url = url
        self.parse = parse

class Spider(object):
    pass
class BaseQylSpider(object):
    pass
