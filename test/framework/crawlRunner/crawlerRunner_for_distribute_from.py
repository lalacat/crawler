import pymongo
import queue
import time
import logging

from queue import Empty
from typing import Iterable

from twisted.internet import task, defer
from twisted.internet.defer import DeferredList, inlineCallbacks

from test.framework.log.log import LogFormat
from test.framework.objectimport.loadobject import load_object
from test.framework.crawlRunner.crawler_for_distribute import Crawler
from test.framework.setting import Setting
from test.framework.utils.reactor import CallLaterOnce

logger = logging.getLogger(__name__)


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

    def __init__(self,settings=None,spidercls=None):
        if isinstance(settings, dict) or settings is None:
            settings = Setting(settings)
        self.settings = settings

        self.lfs = load_object(self.settings['LOG_FORMATTER_CLASS'])
        self.lfm = self.lfs.from_settings(self.settings)

        # self.lfm = LogFormat.from_settings(self.settings)
        logger.debug(*self.lfm.crawled(
            "CrawlerRunner", '',
            '已初始化...')
                     )

        self.spider_loder = []
        # 装载的是Crawler的集合
        self._crawlers = set()
        # 装载的是defer的集合
        self._active = set()
        # 子爬虫的数量
        self.MAX_CHILD_NUM = 9
        if not spidercls:
            # 子爬虫的类
            self.spidercls = spidercls
        else :
            # 从设置中导入子爬虫的类
            self.spidercls = load_object(self.settings['SPIDER_CHILD_CLASS'])

        #  task完成标志位
        self.task_finish = False
        self.slot = None

        self.running = False
        self._task_schedule = queue.Queue()

    def crawl(self, crawler_or_spidercls, *args, **kwargs):

        crawler = self._load_starturl_from_schedule(crawler_or_spidercls)
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

    def _load_starturl_from_schedule(self,spidercls):
        try:
            start_urls = self._task_schedule.get(block=False)
            if isinstance(start_urls,dict):
                name = [key for key in start_urls.keys()][0]
                start_url = [value for value in start_urls.values()][0]
            else:
                start_url = start_urls
                name = start_url.split('/')[-2]
            # logger.debug("当前爬取的网页是:%s"%start_urls)
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", name,
                '当前爬取的网页',start_url)
                         )
            # crawler = self.create_crawler()
            crawler = Crawler(self.spidercls, self.settings,self.lfm)
            crawler._create_spider_from_task(name,start_url)
        except Empty:
            logger.debug("task 分配完毕！！！！")
            self._create_task()
            crawler = None
        except Exception as e :
            logger.error(e)
        return crawler

    @classmethod
    def task_from(cls,db_or_iter,setting=None,spidercls=None,):
        if isinstance(db_or_iter,Iterable):
            cls._task_from_iter = db_or_iter
            cls._task_from_db = None
        if isinstance(db_or_iter,pymongo.cursor.Cursor):
            cls._task_from_iter = None
            cls._task_from_db = db_or_iter
        return cls(spidercls,setting)

    def _create_task(self):
        if self._task_from_db:
            # logger.debug("载入来自db的task!!!!")
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", '',
                '载入来自db的task')
                         )
            try:
                next_task = self._task_from_db.next()
                #  task_name = next_task["total_zone_name"][0]
                for name, url in next_task.items():
                    if name != 'total_zone_name':
                        # logger.debug("%s加载入任务队列中"%url)
                        logger.debug(*self.lfm.crawled(
                            "CrawlerRunner", '',
                            '加载入任务队列中',
                            url)
                                     )
                        self._task_schedule.put(url)
                return
            except StopIteration:
                # logger.debug("来自db的task载入完毕")
                logger.debug(*self.lfm.crawled(
                    "CrawlerRunner", '',
                    '来自db的task载入完毕')
                             )
                self.task_finish = True
                return
            except AttributeError:
                logger.error("task载入类型错误")

        if self._task_from_iter:
            # logger.debug("载入来自iter的task!!!")
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", '',
                '载入来自iter的task')
                         )
            if not hasattr(self._task_from_iter,"_next__"):
                self._task_from_iter = iter(self._task_from_iter)
            while True:
                try:
                    self._task_schedule.put(self._task_from_iter.__next__())
                except StopIteration:
                    # logger.debug("来自iter的task载入完毕")
                    logger.debug(*self.lfm.crawled(
                        "CrawlerRunner", '',
                        '来自iter的task载入完毕')
                                 )
                    self._task_from_iter = None
                    break
                except AttributeError:
                    break
        else:
            # logger.debug("来自iter的task任务结束")
            self.task_finish = True

    def needs_backout(self):
        flag = not self.task_finish and len(self._active) < self.MAX_CHILD_NUM
        return flag

    @inlineCallbacks
    def start(self):
        assert not self.running,"task载入已启动"
        try:
            self.running = True
            self.start_time = time.clock()
            # logger.debug("开始时间是%f"%self.start_time)
            logger.debug(*self.lfm.crawled_time('CrawlerRunner','','开始时间:',
                                                self.start_time))
            nextcall = CallLaterOnce(self.next_task_from_schedule)

            #  将task导入到队列中
            self._create_task()

            self.slot = Slot(nextcall)
            self.slot.nextcall.schedule()
            self.slot.heartbeat.start(5)

            self._closewait = defer.Deferred()
            self._closewait.addBoth(self.stop_task)
            yield self._closewait
        except Exception as e:
            logger.error(e)

    def next_task_from_schedule(self):
        # logger.debug("调用next_task_from_schedule")
        logger.debug(*self.lfm.crawled('CrawlerRunner', '',
                                       '调用next_task_from_schedule'))
        while self.needs_backout():
            self.crawl(self.spidercls)

        if self._active:
            d = DeferredList(self._active)
            return d
        elif self.running:
            self._closewait.callback("Finish")

    def stop_task(self,_):
        logger.debug("任务分配完毕，任务停止")
        slot = self.slot
        slot.heartbeat.stop()
        end_time = time.clock()
        logger.debug("运行时间:%ds" % end_time)
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





