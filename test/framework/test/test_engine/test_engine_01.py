from twisted.internet import defer,reactor,task
from twisted.python.failure import Failure

from test.framework.https.request import Request
from test.framework.https.response import Response
from test.framework.utils.reactor import CallLaterOnce
from test.framework.objectimport.loadobject import load_object
import logging,time


#LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
#DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
#logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
logger = logging.getLogger(__name__)


class Slot(object):
    """
    爬虫过程中，爬虫引擎的插槽
    """
    def __init__(self,start_requests,close_if_idle,nextcall,scheduler):
        """

        :param start_requests: 获取Spider中的爬虫网站
        :param close_if_idle:
        :param nextcall:
        :param scheduler:
        """
        logger.info("卡槽初始化。。。。。。")

        self.closing = False
        self.inprogress = list() #存放正在爬虫的网站,保证每个defer都执行完
        self.start_requests = start_requests
        self.close_if_idle = close_if_idle
        self.nextcall = nextcall
        self.scheduler = scheduler
        # 不断调用方法，通过start和stop控制调用的启停
        self.heartbeat = task.LoopingCall(nextcall.schedule)

    def add_request(self, request):
        """
        :param request:
        :return:
        """
        logger.info("%s 添加到inprogress队列中"%request)
        self.inprogress.append(request)

    def remove_request(self, request):
        #  当request处理完后就可以移除掉了
        self.inprogress.remove(request)
        self._maybe_fire_closing()

    def close(self):
        logger.info("关闭slot")
        self.closing = defer.Deferred()
        self._maybe_fire_closing()
        return self.closing

    def _maybe_fire_closing(self):
        """
        当执行close方法后，self.closing不为False，而且要保证在执行的爬虫任务都要完成的情况下，
        才能够停止心跳函数
        :return:
        """
        if self.closing and not self.inprogress:
            if self.nextcall:
                logger.info("LoopCall关闭")
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)


class ExecutionEngine(object):
    """
    引擎：所有调度
    """

    def __init__(self,crawler,spider_closed_callback):
        logger.debug("引擎初始化")
        self.crawler =crawler
        self.settings = crawler.settings
        # 获取log的格式
        self.logformatter = crawler.logformatter

        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False

        # 从settings中找到Scheduler调度器，找到Scheduler类
        self.scheduler_cls = load_object(self.settings["SCHEDULER"])
        # 同样，找到Downloader下载器类
        downloader_cls = load_object(self.settings["DOWNLOADER"])
        self.downloader = downloader_cls(crawler)
        self.crawlling = []
        self._spider_closed_callback = spider_closed_callback

        self.flag = False

    @defer.inlineCallbacks
    #将爬虫中的网页读取出来
    def open_spider(self,spider,start_requests,close_if_idle=True):
        logger.info("爬虫准备工作开始")
        logger.info("Spider(%s)正在打开"%spider.name,extra = {'spider':spider})
        assert self.has_capacity(),"此引擎已经在处理爬虫了，所以不能处理%s %r" %\
            spider.name
        # 将_next_request注册到reactor循环圈中，便于slot中loopCall不断的调用
        #  相当于不断调用_next_request(spider)
        try:
            nextcall = CallLaterOnce(self._next_request,spider)
            #  初始化scheduler
            scheduler = self.scheduler_cls.from_crawler(self.crawler)
            #  调用中间件，就是添加若干个inner_derfer
            start_requests = yield start_requests
            #  封装Slot对象
            slot = Slot(start_requests,close_if_idle,nextcall,scheduler)
            self.slot = slot
            self.spider = spider
            # 调用scheduler的open
            yield scheduler.open(spider)
            #  启动页面读取，进行爬虫工作

            # 如果start_requests有数据且不需要等待
            while slot.start_requests:
                try:
                    request = next(slot.start_requests)
                except StopIteration:
                    logger.error("网站读取完毕")
                    slot.start_requests = None
                except Exception:
                    slot.start_requests = None
                    logger.error('Error while obtaining start requests',
                                 exc_info=True, extra={'spider': spider})
                #  没有发生异常执行此段代码
                else:
                    self.crawl(request, spider)
            slot.nextcall.schedule()
            #  自动调用启动，每5秒一次调用
            # slot.heartbeat.start(5)
        except Exception as e:
            logger.error(e)

    @defer.inlineCallbacks
    def start(self):
        assert not self.running,"引擎已启动" #running为Flase的时候，不报错，为True的时候，报错
        self.start_time = time.time()
        logger.info("引擎开始时间为: %d" %self.start_time)
        self.running = True
        self._closewait = defer.Deferred()
        yield self._closewait

    def stop(self):
        assert self.running,"引擎没有运行"
        logger.info("停止引擎")
        self.running = False
        dfd = self._close_all_spider()
        dfd.addBoth(lambda _:logger.info("引擎运行 %ds"%(time.time()-self.start_time)))
        dfd.addBoth(lambda _: self._finish_stopping_engine())
        return dfd

    def _finish_stopping_engine(self):
        self._closewait.callback(None)

    def pause(self):
        """
        Pause the execution engine
        此时循环还在进行中，只不过限制了_next_request进行下一步操作
        """
        self.paused = True

    def unpause(self):
        """Resume the execution engine"""
        self.paused = False

    def _next_request(self,spider):
        """
        爬虫爬网页的主要运行方法
        首先是判断slot和引擎的状态，
        其次是通过scheduler对队列中的request进行下载
        最后才是通过start_requset不断将request添加到scheduler中去
        scheduler队列中的request保持在一个，只有下载结束了才会去取新的一个
        :param spider:
        :return:
        """
        logger.debug("调用next_request")

        slot = self.slot
        if not slot:
            return

        if self.paused:
            return

        # 是否等待，因为在opeb_spider中通过nextcall中的LoopCall不断的调用
        # _next_requset必须设置flag来保障，每次调用的时候只有前一次的处理结束
        # 后才能继续执行新的任务
        while not self._needs_backout():
            # 从scheduler中获取request
            # 注意：第一次获取时，是没有的，也就是会break出来从而执行下面的逻辑
            # 当scheduler的request队列为空后，就break
            if not self._next_request_from_scheduler(spider):
                break



        if self.spider_is_idle() and slot.close_if_idle:
            self._spider_idle(spider)

    def _needs_backout(self):
        slot = self.slot
        """
        判断爬虫的状态判断是否需要等待：
        只要有一个False返回False,全True返回True
        1.引擎是否正在运行,默认是False，执行完start后为True
        2.slot是否关闭了,默认slot.closing是False
        3.downloader下载超过预设默认是16个，同时下载的页面超过16个就返回ture
        4.scraper处理response超过预设
        """
        return not self.running \
            or slot.closing \
            or self.downloader.needs_backout()
            #or self.scraper.slot.needs_backout()

    def _next_request_from_scheduler(self,spider):
        #  从scheduler队列中获取request
        #  并进行下载
        slot = self.slot
        request = slot.scheduler.next_request()
        if not request:
            return
        d = self._download(request,spider)
        d.addBoth(self._handle_downloader_output,request,spider)
        d.addErrback(lambda f: logger.info('Error while handling downloader output',
                                       extra={'spider': spider}))

        #  移除掉处理过的request
        d.addBoth(lambda _: slot.remove_request(request))
        d.addErrback(lambda f: logger.info('Error while scheduling new request',
                                           extra={'spider': spider}))

        #  进行下一次的处理request
        d.addBoth(lambda _: slot.nextcall.schedule())
        d.addErrback(lambda f: logger.info('Error while scheduling new request',
                                           extra={'spider': spider}))
        return d

    def _handle_downloader_output(self,response,request,spider):
        #  得到的是下载后的结果，此方法是将结果输出到其他需要处理结果的地方
        assert isinstance(response, (Request, Response, Failure)), response
        if isinstance(response, Request):
            #  到这一步得到的response还是Request类，表明下载不成功，
            #  需要重新走一遍流程
            self.crawl(response, spider)
            return
        # 自己添加处理方法

        return response

    def spider_is_idle(self):

        if self.downloader.active:
            #  判断active队列是否为空，不为空就返回False
            return False

        if self.slot.start_requests is not None:
            return False

        if self.slot.scheduler.has_unhandler_requests():
            return False

        return True

    def _download(self,request,spider):

        slot = self.slot
        #  将取得的requst添加到in_progress中
        slot.add_request(request)

        def _on_success(response):
            #  若得到的是response数据，则就返回response
            logger.info("%s 下载成功"%request.url)
            assert isinstance(response,(Response,Request))
            if isinstance(response,Response):
                response.requset = request
                return response

        def _on_complete(_):
            #  当一个requset处理完后，就进行下一个处理
            slot.nextcall.schedule()
            return _

        dwld = self.downloader.fetch(request,spider)
        dwld.addCallbacks(_on_success,)
        dwld.addBoth(_on_complete)
        return dwld

    @property
    def open_spiders(self):
        return [self.spider] if self.spider else []

    def crawl(self, request, spider):
        assert spider in self.open_spiders, \
            "Spider %r not opened when crawling: %s，即%r 没有执行open_spider方法" % (spider.name, request,spider.name)
        #  添加到队列中去
        self.schedule(request, spider)
        #self.slot.nextcall.schedule()

    def has_capacity(self):
        """保证一个engine对应对应处理一个spider,一个slot对应一个spider"""
        return not bool(self.slot)

    def schedule(self, request, spider):
        logger.debug("%s 进入队列中" %request)
        self.slot.scheduler._mqpush(request)

    def _finish_stopping_engine(self):
        logger.info("finish")
        self._close.callback(None)

    def _spider_idle(self,spider):
        if self.spider_is_idle():
            d = self.close_spider(spider,reason="finished")
            d.addBoth(lambda _:reactor.stop())

    def close_spider(self,spider,reason='cancelled'):
        """关闭所有的爬虫和未解决的requests"""
        slot = self.slot
        if slot.closing:
            # 不是False，就是Defferred对象，就表明已经关闭了
            return slot.closing
        logger.info("将关闭爬虫%(name)s：(%(reason)s)",
                    {
                        'name' :spider.name,
                        'reason': reason
                    },
                    extra={'spider': spider})
        dfd = slot.close()

        def log_failure(msg):
            def errback(failure):
                logger.error(
                    msg,
                    extra={'spider': spider}
                )
            return errback

        #  关闭下载器
        dfd.addBoth(lambda _: self.downloader.close())
        dfd.addErrback(log_failure('Downloader close failure'))

        #  关闭scheduler
        #dfd.addBoth(lambda _: slot.scheduler.close(reason))
        #dfd.addErrback(log_failure('Scheduler close failure'))

        dfd.addBoth(lambda _: logger.info("爬虫%(name)s已关闭：(%(reason)s)",
                    {
                        'name' :spider.name,
                        'reason': reason
                    },
                    extra={'spider': spider}))

        #  引擎中的slot清空
        dfd.addBoth(lambda _: setattr(self, 'slot', None))
        dfd.addErrback(log_failure('Error while unassigning slot'))

        # 引擎中的spider清空
        dfd.addBoth(lambda _: setattr(self, 'spider', None))
        dfd.addErrback(log_failure('Error while unassigning spider'))

        dfd.addBoth(lambda _: self._spider_closed_callback(spider))

        return dfd

    def _close_all_spider(self):
        dfds = [self.close_spider(s, reason='shutdown') for s in self.open_spiders]
        dlist = defer.DeferredList(dfds)
        return dlist
