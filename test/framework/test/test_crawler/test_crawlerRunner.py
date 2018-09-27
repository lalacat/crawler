import queue

from twisted.internet.defer import DeferredList, inlineCallbacks

from test.framework.core.crawler import Crawler
from test.framework.setting import Setting
from test.framework.test.test_spider.simple_spider_01 import SimpleSpider
import logging

logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)


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


    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        crawler = self.check_spider_task(crawler_or_spidercls)
        if crawler is None:
            return None
        return self._crawl(crawler, *args, **kwargs)

    def _crawl(self, crawler, *args, **kwargs):
        self._crawlers.add(crawler)
        d = crawler.crawl(*args, **kwargs)
        self._active.add(d)

        def _done(result):
            # 当已装载的爬虫运行完后，从列表中清除掉
            self._crawlers.discard(crawler)
            self._active.discard(d)
            return result

        return d.addBoth(_done)

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
            start_urls = self.task_schedule.get(block=False)
            name = start_urls.split('/')[-2]
            crawler = self.create_crawler(spidercls)
            crawler._create_spider()
            crawler._spider.start_urls = start_urls
            crawler._spider.name = name
        except Exception as e :
            print(e)
            logger.debug("task 分配完毕！！！！")
            crawler = None
        return crawler

    def stop(self):
        #  停止
        # Stops simultaneously all the crawling jobs taking place.
        # Returns a deferred that is fired when they all have ended.

        return DeferredList([c.stop() for c in list(self._crawlers)])

    @inlineCallbacks
    def join(self):
        '''
        当所有的crawler完成激活之后，返回已经激活的defer的列表
        '''
        while self._active:
            yield DeferredList(self._active)


zone_name = "yangpu"
town_urls = [
    'https://sh.lianjia.com/xiaoqu/anshan/',
    'https://sh.lianjia.com/xiaoqu/dongwaitan/',
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/'
]

top_task = queue.Queue()
for url in town_urls:
    top_task.put(url)

def spider_has_task(spider):
    return spider.start_urls


s = Setting()
cr = CrawlerRunner(top_task,s)
cr.crawl(SimpleSpider)
print(cr._active)
