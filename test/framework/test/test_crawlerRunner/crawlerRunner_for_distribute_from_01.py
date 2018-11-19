import pymongo
import queue
import time
import logging

from queue import Empty
from typing import Iterable

from twisted.internet import task, defer
from twisted.internet.defer import DeferredList, inlineCallbacks

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

    def __init__(self,tasks,settings=None,spidercls=None):
        if isinstance(settings, dict) or settings is None:
            settings = Setting(settings)
        self.settings = settings

        self.lfs = load_object(self.settings['LOG_FORMATTER_CLASS'])
        self.lfm = self.lfs.from_settings(self.settings)

        logger.info(*self.lfm.crawled(
            "CrawlerRunner", '',
            '已初始化...')
                     )
        self._tasks = tasks
        self.spider_loder = []
        # 装载的是Crawler的集合
        self._crawlers = set()
        # 装载的是defer的集合
        self._active = set()
        # 子爬虫的数量
        self.MAX_CHILD_NUM = 9
        # 子爬虫的名称
        # self.SPIDER_NAME_CHOICE = self.settings['SPIDER_NAME_CHOICE']
        self.SPIDER_NAME_CHOICE = False
        # 缓冲的地址最大数量
        self.MAX_SCHEDULE_NUM = 10
        if not spidercls:
            # 子爬虫的类
            self.spidercls = spidercls
        else :
            # 从设置中导入子爬虫的类
            self.spidercls = load_object(self.settings['SPIDER_CHILD_CLASS'])

        #  task完成标志位
        self.filter_task = FilterTask(self.SPIDER_NAME_CHOICE)
        self.task_finish = False
        self._next_task = None

        self.slot = None

        self.running = False
        self._task_schedule = queue.Queue()

    def crawl(self, *args, **kwargs):

        crawler = self._load_starturl_from_schedule()
        if crawler is None:
            return None
        return self._crawl(crawler, *args, **kwargs)

    def _crawl(self, crawler, *args, **kwargs):
        d = crawler.crawl(*args, **kwargs)
        self._crawlers.add(crawler.spider.name)

        def _done(result):
            # 当已装载的爬虫运行完后，从列表中清除掉
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", '',
                '从队列中清除掉{0}'.format(crawler.spider.name))
                         )
            self._crawlers.discard(crawler.spider.name)
            self._active.discard(d)
            return result

        def _next_slot(_):
            self.slot.nextcall.schedule()
            return _

        d.addBoth(_done)
        d.addBoth(_next_slot)
        self._active.add(d)

    def _load_starturl_from_schedule(self):
        try:
            start_urls = self._task_schedule.get(block=False)
            name = start_urls[0]
            start_url = start_urls[1]
            # logger.debug("当前爬取的网页是:%s"%start_urls)
            logger.info(*self.lfm.crawled(
                "CrawlerRunner", name,
                '当前爬取的网页',start_url)
                         )
            crawler = Crawler(self.spidercls, self.settings,self.lfm)
            crawler.create_spider_from_task(name,start_url)
            return crawler
        except Empty:
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", '',
                '"task 分配完毕')
                         )
            self._create_task()
        except Exception as e :
            # logger.error(e)
            logger.error(*self.lfm.error("CrawlerRunner","",
                                         "",
                                         '出现错误:',),
                         extra=
                         {
                             'exception': e,
                         }, exc_info=True)
        return None

    def _create_task(self):
        logger.info(*self.lfm.crawled(
            "CrawlerRunner", '',
            'task装载入队列中')
                     )
        try:
            while self._task_schedule.qsize() <= self.SPIDER_NAME_CHOICE:
                # logger.debug(*self.lfm.crawled(
                #     "CrawlerRunner", '',
                #     '加载入任务队列中')
                #              )
                if self._next_task is None:
                    self._next_task = self.filter_task(next(self._tasks))
                if isinstance(self._next_task,tuple):
                    self._task_schedule.put(self._next_task)
                else:
                    try:
                        self._task_schedule.put(next(self._next_task))
                    except StopIteration:
                        self._next_task = None
                return
        except StopIteration:
            # logger.debug("来自db的task载入完毕")
            logger.debug(*self.lfm.crawled(
                "CrawlerRunner", '',
                '来自db的task载入完毕')
                         )
            self.task_finish = True
            return


    def needs_backout(self):
        flag = not self.task_finish and len(self._active) < self.MAX_CHILD_NUM
        return flag

    @inlineCallbacks
    def start(self):
        assert not self.running,"task载入已启动"
        try:
            self.running = True
            # logger.debug("开始时间是%f"%self.start_time)
            logger.critical(*self.lfm.crawled_time('CrawlerRunner','','开始时间:',
                                                   time.clock()))

            # 将task导入到队列中
            self._tasks = make_generator(self.tasks)
            self._create_task()

            nextcall = CallLaterOnce(self.next_task_from_schedule)
            self.slot = Slot(nextcall)
            self.slot.nextcall.schedule()
            self.slot.heartbeat.start(5)

            self._closewait = defer.Deferred()
            self._closewait.addBoth(self.stop_task)
            yield self._closewait
        except Exception as e:
            logger.error(*self.lfm.error("CrawlerRunner", "",
                                         "",
                                         '出现错误:', ),
                         extra=
                         {
                             'exception': e,
                         }, exc_info=True)

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
        # logger.debug("任务分配完毕，任务停止")
        slot = self.slot
        slot.heartbeat.stop()
        end_time = time.clock()
        logger.critical(*self.lfm.crawled_time('CrawlerRunner', '',
                                '任务分配完毕，任务停止,时间为:',
                                            end_time,))
        # logger.debug("运行时间:%ds" % end_time)
        self.task_finish = False
        return None


class FilterTask(object):

    def __init__(self,settings= None):
        # 子爬虫的名称
        # self.SPIDER_NAME_CHOICE = settings['SPIDER_NAME_CHOICE']
        self.SPIDER_NAME_CHOICE = False
        self.name_num = 0
        # self.filter_words = settings['TASK_FILTER_NAME']
        self.filter_words = 'community_url'

    """
    传入的task类型有三种
    1.迭代前是list的列表，传入后，需要默认添加名称：SPIDER_NAME_CHOICE = Ture
    2.迭代前是数据的游标，传入后分两种，
        a)每个task中包含多个URL，此时数据库中每个对象的格式应该是dict类型{name:url}，此时name,url可以分别取task中的每个dict内容
        b)每个task中只含有一个URL，此时使用关键字就行，name需要使用默认添加名称
    """
    def filter(self,task):
        if self.SPIDER_NAME_CHOICE:
            name = str(self.name_num)
            self.name_num += 1
            if isinstance(task,str):
                url = task
            else:
                url = task[self.filter_words]
        else:
            if isinstance(task, dict):
                if len(task) == 1:
                    name = [key for key in task.keys()][0]
                    url = [value for value in task.values()][0]
                else:
                    return make_generator(task)
            else:
                raise TypeError('task({0})的类型必须是<dict>，或者将{SPIDER_NAME_CHOICE}设置为True，自动为每个task设置名称'.format(type(task)))
        return (name, url)


def make_generator(tasks):
    try:
        it = iter(tasks)
    except Exception as e:
        # logger.error(*self.lfm.error("CrawlerRunner", '',
        #                              'tasks不能被迭代',
        #                              '_make_generator'),
        #              extra={
        #                  'exception': e
        #              })
        raise TypeError('tasks不能被迭代')
    while True:
        try:
            yield it.__next__()
        except StopIteration:
            break
