from twisted.internet import defer,reactor,task
from urllib.parse import quote

from test.framework.engine.reactor import CallLaterOnce
from test.framework.test_import.loadobject import load_object
from test.framework.url_convert import safe_url_string
import logging,time
from test.framework.scheduler.test_scheduler import Scheduler


LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
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
        logger.debug("卡槽初始化。。。。。。")

        self.closing = False
        self.inprogress = set() #存放正在爬虫的网站,保证每个defer都执行完
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
        self.inprogress.add(request)

    def remove_request(self, request):
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
                logger.info("LoopCall取消")
                self.nextcall.cancel()
                if self.heartbeat.running:
                    self.heartbeat.stop()
            self.closing.callback(None)
            reactor.stop()


class ExecutionEngine(object):
    """
    引擎：所有调度
    """

    def __init__(self,crawler,spider_closed_callback):
        logger.debug("引擎初始化")
        self.crawler =crawler
        self.settings = crawler.settings
        #获取log的格式
        self.logformatter = crawler.logformatter

        self.slot = None
        self.spider = None
        self.running = False

        self.scheduler_cls = load_object(self.settings["SCHEDULER"])


        self.crawlling = []
        self._spider_closed_callback = spider_closed_callback

        self.flag = False


    @defer.inlineCallbacks
    def start(self):
        assert not self.running,"引擎已启动" #running为Flase的时候，不报错，为True的时候，报错
        self.start_time = time.time()
        print(self.start_time)
        logger.info("engine start: %d",self.start_time)

        #yield 信号处理
        self.running = True

        self._closewait = defer.Deferred()
        yield self._closewait


    def stop(self):
        assert self.running,"引擎没有运行"
        logger.info("停止引擎")
        self.running = False
        self._closewait.callback(None)

    def _next_request(self,spider):
        """
        爬虫爬网页的主要运行方法
        :param spider:
        :return:
        """
        print("不断调用next_request")

        slot = self.slot
        ''' 
        try:
            self.spider += spider
            logger.info(self.spider)

            if self.spider == 5:
                self.flag = True
            if self.flag:
                logger.info("心跳停止")
                self.slot.close()

        except Exception as e:
            print(e)
        '''
        # 是否等待，因为在opeb_spider中通过nextcall中的LoopCall不断的调用
        # _next_requset必须设置flag来保障，每次调用的时候只有前一次的处理结束
        # 后才能继续执行新的任务
        while not self._needs_backout():
            # 从scheduler中获取request
            # 注意：第一次获取时，是没有的，也就是会break出来
            # 从而执行下面的逻辑
            pass

        # 如果start_requests有数据且不需要等待
        if slot.start_requests and not self._needs_backout():
            pass

    def _needs_backout(self):
        slot = self.slot
        """
        判断爬虫的状态判断是否需要等待：
        只要有一个False返回False,全True返回True
        1.引擎是否正在运行
        2.爬虫的状态管理类是否关闭了
        3.downloader下载超过预设
        4.scraper处理response超过预设
        """
        return not self.running \
            or slot.closing \
            #or self.downloader.needs_backout() \
            #or self.scraper.slot.needs_backout()

    def print_web(self,content):

        for items in content:
            for key,value in items.items():
                print(key,value)


    #当一个defer爬虫结束后，将完成的爬虫线程从list中移除去
    def finish_crawl(self,content,req):
        logger.info("finish")
        self.crawlling.remove(req)
        return content

    def crawl_err(self,content,req):
        logger.error("error found \n",content)
        self.crawlling.remove(req)
        return None

    @defer.inlineCallbacks
    #将爬虫中的网页读取出来
    def open_spider(self,spider,start_requests,close_if_idle=True):
        logger.info("爬虫准备工作开始")
        logger.info("Spider正在打开",extra = {'spider':spider})
        assert self.has_capacity(),"此引擎已经在处理爬虫了，所以不能处理%s %r" %\
            spider.name
        # 将_next_request注册到reactor循环圈中，便于slot中loopCall不断的调用
        #  相当于不断调用_next_request(spider)
        try:
            self.spider = spider
            nextcall = CallLaterOnce(self._next_request,spider)
            #  初始化scheduler
            scheduler = self.scheduler_cls.from_crawler(self.crawler)
            #  调用中间件，就是添加若干个inner_derfer
            #  start_requests = yield start_requests
            slot = Slot(start_requests,close_if_idle,nextcall,scheduler)
            self.slot = slot
            print("1")

            yield self.scheduler_cls.open(spider)

            #  启动页面读取，进行爬虫工作
            slot.nextcall.schedule()
            #  自动调用启动，每5秒一次调用
            slot.heartbeat.start(1)
        except Exception as e:
            logger.error(e)

    def has_capacity(self):
        """保证一个engine对应对应处理一个spider,一个slot对应一个spider"""
        return not bool(self.slot)

    def _finish_stopping_engine(self):
        logger.info("finish")
        self._close.callback(None)

