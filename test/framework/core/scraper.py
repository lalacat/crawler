import logging
import time
from collections import deque, Iterable

from twisted.internet import defer
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

from test.framework.https.request import Request
from test.framework.https.response import Response
from test.framework.core.item import BaseItem
from test.framework.middleware.itempipelinemw import ItemPipelineManager
from test.framework.middleware.spidermw import SpiderMiddlewareManager
from test.framework.utils.defer import defer_result, defer_succeed, iter_errback, parallel
from test.framework.utils.exception import CloseSpider

logger = logging.getLogger(__name__)


class Slot(object):
    """Scraper slot (one per running spider)"""

    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        #  通过记active_size来判断是否需要等待request处理结束
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def add_response_request(self, response, request):
        #  添加序列，记录处理的大小
        deferred = defer.Deferred()
        self.queue.append((response, request, deferred))
        if isinstance(response, Response):
            self.active_size += max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE
        return deferred

    def next_response_request_deferred(self):
        #  先进先出
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
        #  当set()或者deque()为空的时候，返回的是false
        return not (self.queue or self.active)

    def needs_backout(self):
        return self.active_size > self.max_active_size


class Scraper(object):

    def __init__(self,crawler):
        self.crawler = crawler
        self.lfm = crawler.logformatter
        logger.debug(*self.lfm.crawled("Spider", crawler.spider.name,
                                       '已初始化...', 'Scraper'))
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        #  itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = ItemPipelineManager.from_crawler(crawler)

        #  单次最多能处理最大的item的个数
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler

    @defer.inlineCallbacks
    def open_spider(self,spider):
        # logger.debug("Spider:%s 的Scraper已打开..."%spider.name)
        logger.debug(*self.lfm.crawled("Spider", spider.name,
                                       '已打开...', 'Scraper'))
        self.slot = Slot()
        self.spider = spider
        yield self.itemproc.open_spider(spider)

    def close_spider(self, spider):
        # logger.info("关闭 %s 的Scraper！！"%spider.name)
        logger.warning(*self.lfm.crawled("Spider", spider.name,
                                       '已关闭...', 'Scraper'))
        slot = self.slot
        slot.closing = defer.Deferred()
        #  对所有的itemproc进行并行关闭
        slot.closing.addCallback(self.itemproc.close_spider)
        self._check_if_closing(spider, slot)
        return slot.closing

    def is_idle(self):
        """Return True if there isn't any more spiders to process"""
        return not self.slot

    def _check_if_closing(self, spider, slot):
        if slot.closing and slot.is_idle():
            slot.closing.callback(spider)

    def enqueue_scrape(self, response, request, spider):
        self.start_time = time.clock()
        # logger.info("%s.%s的response加入scrapy队列,加入时间为：%7.6f"%(spider.name,request,self.start_time))
        logger.info(*self.lfm.crawled_time("Spider", spider.name, 'response加入队列时间', time.clock(), 'Scraper'))
        slot = self.slot
        dfd = slot.add_response_request(response, request)

        def finish_scraping(_):
            slot.finish_response(response, request)
            self._check_if_closing(spider, slot)
            self._scrape_next(spider, slot)
            return _

        def log_error(_):
            # print(_.getErrorMessage())
            logger.error(*self.lfm.error("Spider", self.spider.name,
                                            {
                                                'function': 'Scraper',
                                                'request': request
                                            },
                                            '处理出现错误:'),
                         exc_info = True,
                         extra={'exception':_.getErrorMessage()})

        dfd.addBoth(finish_scraping)
        # dfd.addErrback(lambda f: logger.error('Scraper 处理 %(request)s的结果时，出现出现错误！！\n'
        #                                       '错误信息为：%(error)s',
        #                            {'request': request,"error":f}
        #                            ))
        dfd.addErrback(log_error)

        self._scrape_next(spider, slot)
        return dfd

    def _scrape_next(self, spider, slot):
        while slot.queue:
            response, request, deferred = slot.next_response_request_deferred()
            self._scrape(response, request, spider).chainDeferred(deferred)

    def _scrape(self, response, request, spider):
        """Handle the downloaded response or failure through the spider
        callback/errback"""
        assert isinstance(response, (Response, Failure))
        #  如果结果没有出错的时候，先进行中间件的处理，然后执行在request中或者是spider中定义的callback或者是_parse来处理结果
        #  结果处理完后执行自定义的规则，将结果进行制定规则的输出
        dfd = self._scrape2(response, request, spider)  # returns spiders processed output
        dfd.addErrback(self.handle_spider_error, request,response, spider)
        dfd.addCallback(self.handle_spider_output, request, response, spider)
        return dfd

    def _scrape2(self, request_result, request, spider):
        """Handle the different cases of request's result been a Response or a
        Failure"""
        if not isinstance(request_result, Failure):
            return self.spidermw.scrape_response(self.call_spider, request_result, request, spider)
        else:
            #
            dfd = self.call_spider(request_result, request, spider)
            dfd.addErrback(self._log_download_errors, request_result, request, spider)
            return dfd

    def call_spider(self, result, request, spider):
        middle_time = time.clock()
        # logger.info("通过%s._parse处理结果,时间为：%f"%(spider.name,middle_time))

        result.request = request
        dfd = defer_result(result)
        #  这一步才是真正意义上的处理爬到的结果，之前的都是在过滤错误
        dfd.addCallbacks(request.callback or spider.parse, request.errback)
        return dfd

    def handle_spider_error(self, _failure, request, response, spider):
        exc = _failure.value
        end_time = time.clock()
        # logger.error("%(request)s处理结果的时候出现错误：\n%(failure)s\nprocess item 持续时间"
        #              "为：%(time)f",
        #              {"request":request,"failure":exc,"time":(end_time-self.start_time)})

        logger.error(*self.lfm.error('Spider',self.spider.name,
                                     {
                                         'function':'Scraper',
                                         'request':request
                                     },'处理结果的时候出现错误')
                     ,extra={
                        'exception':exc,
                        'time':'处理结果时间为：{:6.3f}s'.format(end_time-self.start_time)
                    },exc_info = True)
        if isinstance(exc,CloseSpider):
            self.crawler.engine.close_spider(spider,exc or "cancelled")

    def handle_spider_output(self, result, request, response, spider):
        """
        通过spider._parse或者request.callback处理后的数据，可能会根据需要，返回None或者Request，可迭代型的list,dict,或者是yield 生成器
        其中生成器是无法测定具体的大小的，所以不能用len()来确定并行处理task的数目
        并行处理task的数目100和20的区别并不大

        :param result:
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if not result:
            # logger.warning("%s._parse或者request.callback返回的结果为None,不经过自定义process_item 处理！！"%spider.name)
            logger.warning(*self.lfm.crawled('Spider',spider.name,
                                             '_parse(callback)',
                                             '返回的结果为<None>,不经过自定义{process_item}处理'))
            return defer_succeed(None)
        if isinstance(result,Request):
            #  针对是return 当spider处理后的结果是yield，那么result的类型是generator
            self.crawler.engine.crawl(request=result, spider=spider)
            return defer_succeed(result)
        if not isinstance(result,Iterable):
            # logger.warning("%s._parse或者requst.callback处理的结果不是<Iterable>，而是%s类型的数据,不能通过pipe处理！！"%(spider.name,type(result)))
            logger.warning(*self.lfm.crawled('Spider', spider.name,
                                             '_parse(callback)',
                                             '处理的结果是{1}类型,不是<Iterable>,不能经过自定义<pipe>处理'.format(type(result))))
            return defer_succeed(result)
        #  将自定义处理好的结果，通过这个方法并行执行自定义的rule（pipe process_item）
        #  这里的结果默认是能够迭代的List或者是dict类型的结果，每个结果都是并列的，能够同时符合process_item处理规则
        #  其中list里的结果是两种类型，一种是BaseItem及其子类一种是dict类型，这些都是在requst或者spider中自己
        #  处理后的得到的
        # logger.debug("%s的parse处理后的结果类型是%s,下一步进行process_item并行处理"%(spider.name,type(result)))
        logger.debug(*self.lfm.crawled('Spider', spider.name,
                                         '_parse(callback)',
                                         '处理后的结果类型是{0},下一步进行process_item并行处理'.format(type(result))))
        it = iter_errback(result, self.handle_spider_error, request, response, spider)

        dfd = parallel(it,self.concurrent_items,self._process_spidermw_output, request, response, spider)
        dfd.addCallback(self._process_item_time)
        return dfd

    def _process_spidermw_output(self, output, request, response, spider):
        """Process each Request/Item (given in the output parameter) returned
        from the given spider
        """
        # logger.debug("在并行处理中。。。。。。。。")
        logger.debug(*self.lfm.crawled("Spider", spider.name,
                               '并行处理中',
                               {
                                   'function': 'Scraper',
                                   'request': request
                               }))
        if isinstance(output, Request):
            # logger.info("处理的output%(request)s的类型是<Request>，将添加到下载序列中！！添加时间是：%(time)f",{"request":output,"time":time.clock()})
            logger.info(*self.lfm.crawled_time('Spider',spider.name,'Output的类型是<Request>,将添加到下载队列中,加入时间:',time.clock(),output))
            self.crawler.engine.crawl(request=output, spider=spider)
        elif isinstance(output, (BaseItem, dict,int)):
            # logger.info("处理的output%(request)s的类型是<BaseItem, dict,int>，
            # 将由自定义的process_item方法进行处理！！添加时间是：%(time)f",
            # {"request":output,"time":time.clock()})
            logger.info(*self.lfm.crawled_time('Spider',spider.name,'Output的类型是<BaseItem, dict,int>,将通过自定义的process_item方法进行处理,处理时间:',time.clock(),output))

            self.slot.itemproc_size += 1
            dfd = self.itemproc.process_item(item=output,spider=spider)
            dfd.addBoth(self._itemproc_finished, output, response, spider)

            return dfd

        elif output is None:
            pass

        else:
            typename = type(output).__name__
            # logger.error('Spider must return Request, BaseItem, dict or None, '
            #              'got %(typename)r in %(request)s',
            #              {'request': request, 'typename': typename},
            #              extra={'spider': spider})
            logger.error(*self.lfm.error('Spider',spider.name,
                                       {
                                           'function':'Scraper',
                                           'request':request
                                       },'处理的结果的类型必须是<Request>,<BaseItem>,<dict>,<None>。返回的类型是:')
                         ,extra={'exception':typename})

    def _itemproc_finished(self, output, item, response, spider):
        """ItemProcessor finished for the given ``item`` and returned ``output``
        """
        #  得到的output是一个处理过的items，一般是dict类型的数据
        #  output==item

        self.slot.itemproc_size -= 1
        if isinstance(output, Failure):
            ex = output.value
            # logging.error(ex)
            # logger.error('process item(%(item)s)过程中出现错误', {'item': item})
            logger.error(*self.lfm.error('Spider',spider.name,
                                       {
                                           'function':'Scraper',
                                           'request':item
                                       },'处理过程中出现错误:')
                         ,extra={'exception':ex})
        else:
            # logger.debug("process item(%s)处理完毕"%item,extra={'spider': spider})
            logger.debug(*self.lfm.crawled('Spider',spider.name,'处理完毕',
                                           {
                                               'function': 'Scraper',
                                               'request': item
                                           }
                                           ))
        return None

    def _log_download_errors(self,context,request_result, request, spider):
        # logger.error(context)
        logger.error(*self.lfm.error("Spider", spider.name,
                              {
                                  'function': 'Scraper',
                                  'request': request
                              },
                              '出现错误', ),
                     extra=
                     {
                         'exception': context,
                         'time': "\n时间是{:d}".format(34)
                     })
        return context

    def _process_item_time(self,_):
        end_time = time.clock()
        # logger.info("经过process_item处理后，此时时间为%f,完成Scraper模块使用了%7.6f"%(end_time,end_time-self.start_time))
        logger.debug(*self.lfm.crawled_time("Spider",self.spider.name,
                            'process_item处理完毕后的时间:',
                            end_time,
                            "Scraper"),
                    extra={'extra_info':",完成Scraper模块使用了{:6.3f}".format(end_time-self.start_time)}
                            )
        return None