import logging
from collections import deque

from twisted.internet import defer

from test.framework.https.response import Response
from test.framework.middleware.itempipelinemw import ItemPipelineManager
from test.framework.middleware.spidermw import SpiderMiddlewareManager
from test.framework.objectimport.loadobject import load_object


logger = logging.getLogger(__name__)

class Slot(object):
    """Scraper slot (one per running spider)"""

    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def add_response_request(self, response, request):
        deferred = defer.Deferred()
        self.queue.append((response, request, deferred))
        if isinstance(response, Response):
            self.active_size += max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE
        return deferred

    def next_response_request_deferred(self):
        response, request, deferred = self.queue.popleft()
        self.active.add(request)
        return response, request, deferred

    def finish_response(self, response, request):
        self.active.remove(request)
        if isinstance(response, Response):
            self.active_size -= max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size -= self.MIN_RESPONSE_SIZE

    def is_idle(self):
        return not (self.queue or self.active)

    def needs_backout(self):
        return self.active_size > self.max_active_size

class Scraper(object):

    def __init__(self,crawler):
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        #  itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = ItemPipelineManager.from_crawler(crawler)

        #  单次最多能处理最大的item的个数
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler

    @defer.inlineCallbacks
    def open_spider(self,spider):
        self.slot = Slot()