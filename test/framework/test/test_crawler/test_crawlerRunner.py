import queue
import time
from queue import Empty

from twisted.internet import task, defer
from twisted.internet.defer import DeferredList, inlineCallbacks

from test.framework.crawlRunner.crawler_for_distribute import Crawler
from test.framework.setting import Setting
from test.framework.test.test_spider.simple_spider.simple_spider_04_xiaoqu_db import SimpleSpider
import logging

from test.framework.utils.reactor import CallLaterOnce

logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.CRITICAL,format=LOG_FORMAT,datefmt=DATE_FORMAT)


class Slot(object):
    def __init__(self,nextcall):
        self.closing = False
        self.heartbeat = task.LoopingCall(nextcall.schedule)
        self.nextcall = nextcall
        self.inprogress = list()


    def add_crawl(self,crawl):
        """
        记录正在进行的crawl
        :param crawl:
        :return:
        """
        logger.debug("%s 添加到inprogress队列中" % crawl)
        self.inprogress.append(crawl)

    def remove_crawl(self,crawl):
        self.inprogress.remove(crawl)
        self._maybe_closing()

    def close(self):
        logger.debug("关闭CrawlerRunner的slot")
        self.closing = defer.Deferred()
        self._maybe_closing()
        return self.closing

    def _maybe_closing(self):
        if self.closing and not self.inprogress:
            if self.nextcall:
                logger.warning("CrawlerRunner的LoopCall已关闭")
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)


class CrawlerRunner(object):

    def __init__(self, tasks,settings=None):
        if isinstance(settings, dict) or settings is None:
            settings = Setting(settings)
        self.settings = settings
        self.spider_loder = []
        # 装载的是Crawler的集合
        self._crawlers = set()
        # 装载的是defer的集合
        self._active = set()
        # 子爬虫的数量
        self._childNum = 3
        self.task_schedule = tasks
        self.task_finish = False
        self.slot = None
        self.running = False
        self.searchRes = tasks
        self.child_task = queue.Queue()

    def crawl(self, crawler_or_spidercls, *args, **kwargs):

        crawler = self.check_spider_task(crawler_or_spidercls)
        if crawler is None:
            return None
        return self._crawl(crawler, *args, **kwargs)

    def _crawl(self, crawler, *args, **kwargs):
        d = crawler.crawl(*args, **kwargs)
        self._crawlers.add(crawler.spider.name)

        def _done(result):
            # 当已装载的爬虫运行完后，从列表中清除掉
            logger.debug("从列表中清除掉%s"%crawler.spider.name)
            self._crawlers.discard(crawler.spider.name)
            self._active.discard(d)
            return result

        def _next_slot(_):
            self.slot.nextcall.schedule()
            return _

        d.addBoth(_done)
        d.addBoth(_next_slot)
        self._active.add(d)

    def create_crawler(self, crawler_or_spidercls):

        '''
        先判断传入的参数是不是已经包装成Crawler，如果是，直接返回
        不是的，将传入的参数进行包装，返回成Crawler
        :param crawler_or_spidercls: Crawler的实例，或者是自定义爬虫模块
        :return: Cralwer的实例
        '''

        if isinstance(crawler_or_spidercls, Crawler):
            return crawler_or_spidercls
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        #  判断传入的参数是自定义爬虫的name还是对应的class模块
        if isinstance(spidercls, str):
            logger.debug("传入的是str类型的class")
            spidercls = self.spider_loder.load(spidercls)
        return Crawler(spidercls, self.settings)

    def check_spider_task(self,spidercls):
        try:
            start_urls = self.child_task.get(block=False)
            print("当前爬取的网页是:%s"%start_urls)
            name = start_urls.split('/')[-2]
            crawler = self.create_crawler(spidercls)
            crawler._create_spider()
            crawler._spider.start_urls = start_urls
            crawler._spider.name = name
            logger.debug("爬虫的名称是%s"%name)
        except Empty:
            logger.debug("task 分配完毕！！！！")
            self.load_task()
            crawler = None
        except Exception as e :
            print("check_spider_task",e)
        return crawler

    def load_task(self):
        next_task = self.task_scheduke_next()
        if next_task:
            task_name = next_task["total_zone_name"][0]
            print(task_name)
            for name, url in next_task.items():
                if name != 'total_zone_name':
                    self.child_task.put(url)
            print("========================")
        else:
            print("任务取完")
            self.task_finish = True

    def task_scheduke_next(self):
        try:
            result = self.searchRes.next()
        except StopIteration:
            result = None
        return result

    def needs_backout(self):
        flag = not self.task_finish and len(self._active) < 9
        #flag = not self.task_finish
        return flag

    @inlineCallbacks
    def start(self):
        assert not self.running,"task载入已启动"
        self.running = True
        self.start_time = time.clock()
        nextcall = CallLaterOnce(self.next_task_from_schedule)
        self.load_task()

        self.slot = Slot(nextcall)
        self.slot.nextcall.schedule()
        self.slot.heartbeat.start(5)

        self._closewait = defer.Deferred()
        self._closewait.addBoth(self.stop_task)
        yield self._closewait

    def next_task_from_schedule(self):
        #logger.debug("调用next_task_from_schedule")
        while self.needs_backout():
            self.crawl(SimpleSpider)

        if self._active:
            d = DeferredList(self._active)
            return d
        elif self.running:
            self._closewait.callback(None)


    def stop(self):
        #  停止
        # Stops simultaneously all the crawling jobs taking place.
        # Returns a deferred that is fired when they all have ended.

        return DeferredList([c.stop() for c in list(self._crawlers)])

    def stop_task(self,_):
        logger.debug("任务分配完毕，任务停止")
        slot = self.slot
        slot.heartbeat.stop()
        end_time = time.clock()
        print("运行时间:%ds" % end_time)
        self.task_finish = False
        return None

    @inlineCallbacks
    def join(self):
        '''
        当所有的crawler完成激活之后，返回已经激活的defer的列表
        '''
        while self._active:
            logger.debug("deferlist")
            yield DeferredList(self._active)





