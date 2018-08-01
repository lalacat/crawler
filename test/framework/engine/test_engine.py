from twisted.internet import defer,reactor,task
from twisted.web.client import getPage
from queue import Queue
from urllib.parse import quote
from test.framework.url_convert import safe_url_string
import logging,time


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
        #获取log的格式
        self.logformatter = crawler.logformatter

        self.slot = None
        self.spider = None
        self.running = False

        self.scheduler = None

        self.crawlling = []
        self._spider_closed_callback = spider_closed_callback

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
        solt = self.slot

        # 是否等待
        while not self._needs_backout():
            # 从scheduler中获取request
            # 注意：第一次获取时，是没有的，也就是会break出来
            # 从而执行下面的逻辑
            pass

        # 如果start_requests有数据且不需要等待
        if solt.start_requests and not self._needs_backout():
            pass

        '''
        
        if self.scheduler.qsize() != 0 :
            logger.info("爬虫：%s 还剩下%d个网页"%(spider_name,self.scheduler.qsize()))

        try:

            if self.scheduler.qsize() == 0 and len(self.crawlling) == 0:
                logger.info("爬虫 %s end"%spider_name)
                self._finish_stopping_engine()
                return


            req = self.scheduler.next_request()
            #if req is not None:
            #对即将处理的req存储到临时列表中，这是为了防止其他的req还没处理完，程序就结束了，因为判断程序结束的标志时scheduler的q.size()为0，
            #即任务队列中的数据全部取出来了，但是结束标志中还需要在定义一个标志，表示所有的defer都处理完了，就用crawlling进行处理，任务进行前，
            #先将要进行的任务存储到crawlling列表中，当数据处理完，再将对应的req从列表中去除，当列表为空的时候，证明所有的defer的callback处理完了
            self.crawlling.append(req)
            # 对网页进行编码的处理，防止网页中含有中文字符，程序不能对中文字符进行解析，报错；
            # 对网页进行处理后‘：’也会被解析成“%3A”，所以要对解析后的网页在进行处理将“：”重新代替回来
            #_url = quote(req.url).replace("%3A",":")
            #print(_url)
            _url = safe_url_string(req.url,"utf-8")

            d = getPage(_url.encode('utf-8'))


            # d.addCallback(self.get_response_callback,req)
            #d.addCallback(self.print_web)

            d.addCallback(req.parse,req.url)
            d.addCallback(self.finish_crawl, req)
            if db is not None:
                d.addCallback(db.insert_mongoDb)

            d.addErrback(self.crawl_err,req)
            d.addBoth(lambda _:reactor.callLater(0,self._next_request,spider_name,db))

        except AttributeError as e:
            logger.error("对象没有对应的属性",e)
            return None
        except Exception as e :
            logger.error("Exception",e)
    '''
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
    def open_spider(self,spider,start_requests,db=None):
        logger.info("分解spider")
        yield self.scheduler.open()
        while True:
            try:
                req = next(start_requests)
                logger.info("读取网站:%s"%req.url)
            except StopIteration as e:
                logger.info("网站读取完毕")
                break
            except Exception as e :
                logger.error("在对spider网页导入的操作的过程中出现错误",e)
            self.scheduler.put_request(req)


    def  _finish_stopping_engine(self):
        logger.info("finish")
        self._close.callback(None)

