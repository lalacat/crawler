class BaseSpider(object):
    pass
class Request(object):
    def __init__(self, url, parse):
        self.url = url
        self.parse = parse