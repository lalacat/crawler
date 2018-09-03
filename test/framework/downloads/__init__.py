import datetime
import random
import warnings
import logging
from collections import deque
from time import time

from twisted.internet import defer, task,reactor

from test.framework.crawler import Crawler, _get_spider_loader
from test.framework.https.request import Request
from test.framework.https.response import Response
from test.framework.middleware import MiddlewareManager
from test.framework.objectimport import bulid_component_list
from test.framework.setting import Setting
from test.framework.objectimport.loadobject import load_object
from test.framework.downloads.download_agent import HTTPDownloadHandler
from test.framework.twisted.defer import mustbe_deferred

logger = logging.getLogger(__name__)

class Slot(object):
    """
    Downloader slot
    这个slots是一个存储Slot对象的字典，key是request对应的域名，值是一个Slot对象。
    Slot对象用来控制一种Request下载请求，通常这种下载请求是对于同一个域名。
    这个Slot对象还控制了访问这个域名的并发度，下载延迟控制，随机延时等，
    主要是为了控制对一个域名的访问策略，一定程度上避免流量过大被封IP，不能继续爬取。
    """
    def __init__(self,concurrency,delay,randomize_delay):
        #  并发度，延迟时间和随机延迟
        self.concurrency = concurrency
        self.delay = delay
        self.randomize_delay = randomize_delay

        self.active = set()
        #  双向队列
        self.queue = deque()
        self.transferring = set()
        self.lastseen = 0
        self.latercall = None

    def free_transfer_slots(self):
        return self.concurrency - len(self.transferring)

    def download_delay(self):
        if self.randomize_delay:
            return random.uniform(0.5 * self.delay, 1.5 * self.delay)
        return self.delay

    def close(self):
        if self.latercall and self.latercall.active():
            self.latercall.cancel()

    def __repr__(self):
        cls_name = self.__class__.__name__
        return "%s(concurrency=%r, delay=%0.2f, randomize_delay=%r)" % (
            cls_name, self.concurrency, self.delay, self.randomize_delay)

    def __str__(self):
        return (
            "<downloader.Slot concurrency=%r delay=%0.2f randomize_delay=%r "
            "len(active)=%d len(queue)=%d len(transferring)=%d lastseen=%s>" % (
                self.concurrency, self.delay, self.randomize_delay,
                len(self.active), len(self.queue), len(self.transferring),
                datetime.fromtimestamp(self.lastseen).isoformat()
            )
        )


#  延迟
def _get_concurrency_delay(concurrency, spider, settings):
    delay = settings.getfloat('DOWNLOAD_DELAY')
    if hasattr(spider, 'DOWNLOAD_DELAY'):
        warnings.warn("%s.DOWNLOAD_DELAY attribute is deprecated, use %s.download_delay instead" %
                      (type(spider).__name__, type(spider).__name__))
        delay = spider.DOWNLOAD_DELAY
    if hasattr(spider, 'download_delay'):
        delay = spider.download_delay

    if hasattr(spider, 'max_concurrent_requests'):
        concurrency = spider.max_concurrent_requests

    return concurrency, delay


class Downloader(object):
    def __init__(self,crawler):
        self.settings = crawler.settings
        #  如果只是加载一个类不带参数，而这个类的初始化带有参数的时候，使用这个类的时候会报错
        #  XXX missing X required positional argument
        self.handler = load_object(self.settings["DOWNLOAD_HANDLER"])(self.settings)
        self.slots = {}
        # active是一个活动集合，用于记录当前正在下载的request集合。
        self.active = set()
        # 从配置中获取设置的并发数
        self.total_concurrency = self.settings.getint('CONCURRENT_REQUESTS')
        # 同一域名并发数
        self.domain_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        # 同一IP并发数
        self.ip_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_IP')
        # 随机延迟下载时间
        self.randomize_delay = self.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        # 初始化下载器中间件
        self.middleware = DownloaderMiddlewareManager.from_crawler(crawler)
        # ask.LoopingCall安装了一个60s的定时心跳函数_slot_gc,这个函数用于对slots中的对象进行定期的回收。
        self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        self._slot_gc_loop.start(60)

    #  进行加载中间件，及对requset进行下载
    def fetch(self,request,spider):
        logger.info("加载中间件，准备下载")
        def _deactivate(response):
            self.active.remove(request)
            return response

        self.active.add(request)
        #  调用中间件管理器的download方法，同时传入了自己的_enqueue_request方法。
        #dfd = self.middleware.download(self._enqueue_request, request, spider)
        dfd = self.middleware.download(self._download, request, spider)
        return dfd.addBoth(_deactivate)

    def needs_backout(self):
        return len(self.active) >= self.total_concurrency

    #  处理requset
    def _enqueue_request(self, request, spider):
        key, slot = self._get_slot(request, spider)
        request.meta['download_slot'] = key

        def _deactivate(response):
            slot.active.remove(request)
            return response

        slot.active.add(request)
        deferred = defer.Deferred().addBoth(_deactivate)
        slot.queue.append((request, deferred))
        self._process_queue(spider, slot)
        return deferred

    def _process_queue(self, spider, slot):
        '''
        这个函数通过最下面的while循环处理队列中的请求，并判断当前是否有空闲的传输slot，有空闲的才继续下载处理。
        处理下载请求时，会不断更新slot的lastseen为当前时间，这个值代表了slot的最近一次活跃下载时间。
        :param spider:
        :param slot:
        :return:
        '''

        if slot.latercall and slot.latercall.active(): # 如果一个latercall正在运行则直接返回
            return

        # Delay queue processing if a download_delay is configured
        now = time()
        delay = slot.download_delay() #  获取slot对象的延迟时间
        if delay:
            penalty = delay - now + slot.lastseen # 距离上次运行还需要延迟则latercall
            if penalty > 0:
                slot.latercall = reactor.callLater(penalty, self._process_queue, spider, slot)
                return

        # Process enqueued requests if there are free slots to transfer for this slot
        while slot.queue and slot.free_transfer_slots() > 0:  # 不停地处理slot队列queue中的请求，如果队列非空且有空闲的传输slot,则下载，如果需要延迟则继续调用'_process_queue'
            slot.lastseen = now
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)
            # prevent burst if inter-request delays were configured
            if delay:
                self._process_queue(spider, slot)
                break

    def _download(self, request, spider,slot=None,):
        logger.info("进行下载。。。。。")
        #logger.info("request：%s，spider: %s"%(request,spider))
        try:
            dfd = mustbe_deferred(self.handler.download_request,request,spider)
        except Exception:
            raise ValueError("can't find spider")
        '''
        slot.transferring.add(request)
           def finish_transferring(_):
            slot.transferring.remove(request)
            self._process_queue(spider, slot)
            return _
        '''
        #return dfd.addBoth(finish_transferring)
        return dfd

    def close(self):
        self._slot_gc_loop.stop()
        for slot in iter(self.slots):
            slot.close()

    #  垃圾回收
    def _slot_gc(self, age=60):
        """
        如果一个Slot对象没有正在活动的下载request,且距离上次活动的时间已经过去了60s则进行回收。
        :param age:
        :return:
        """
        mintime = time() - age
        for key, slot in list(self.slots.items()):
            if not slot.active and slot.lastseen + slot.delay < mintime:
                self.slots.pop(key).close()



class DownloaderMiddlewareManager(MiddlewareManager):

    component_name = 'downloader middleware'
    @classmethod
    def _get_mwlist_from_settings(cls,settings):
        return bulid_component_list(settings['TEST_DOWNLOADER_MIDDLEWARE'])

    def _add_middleware(self,mw):
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            self.methods['process_response'].insert(0, mw.process_response)
        if hasattr(mw, 'process_exception'):
            self.methods['process_exception'].insert(0, mw.process_exception)

    def download(self,download_func,request,spider):
        #  将默认处理的三个中间件分别添加到defer链上
        @defer.inlineCallbacks
        def process_request(request):
            logger.info("处理process_request")
            for method in self.methods['process_request']:
                response = yield method(request=request,spider =spider)
                assert response is None or isinstance(response,(Response,Request)),\
                '中间件%s.process_request 执行后返回的数据类型必须是 None,Response或者Request'\
                % method._class__._name__
                #  如果结果是下载后的，就直接返回
                if response:
                    defer.returnValue(response)
            #  如果参数是经过一系列中间件处理过的request，这一步就是对requset进行下载
            #ddf =
            #  返回一个带有result的defer
            try:
                dlf = yield download_func(request=request,spider=spider)
                defer.returnValue(dlf)
                #defer.returnValue((yield download_func(request=request,spider=spider)))
            except Exception as e:
                logger.error("process_request: %s" %e)

        @defer.inlineCallbacks
        def process_response(response):
            logger.info("处理process_response")
            assert response is not None,"process_response接收到的数据是None"
            if isinstance(response,Request):
                defer.returnValue(response)

            for method in self.methods['process_response']:
                response = yield method(request=request, response=response,
                                        spider=spider)
                assert response is None or isinstance(response, (Response, Request)), \
                    '中间件%s.process_request 执行后返回的数据类型必须是 None,Response或者Request' \
                    % method._class__._name__
                if isinstance(response, Request):
                    defer.returnValue(response)
            defer.returnValue(response)

        @defer.inlineCallbacks
        def process_exception(_failure):
            exception = _failure.value
            for method in self.methods['process_exception']:
                response = yield method(request=request, exception=exception,
                                        spider=spider)
                assert response is None or isinstance(response, (Response, Request)), \
                    'Middleware %s.process_exception must return None, Response or Request, got %s' % \
                    (method.__class__.__name__, type(response))
                if response:
                    defer.returnValue(response)
            defer.returnValue(_failure)


        deferred = mustbe_deferred(process_request,request)

        deferred.addErrback(process_exception)
        deferred.addCallback(process_response)
        return deferred

'''
def func_test(result):
    print(result)
s = Setting()

m = DownloaderMiddlewareManager.from_settings(s,"A")


m.methods['test_fun_common'].append(m.methods['Test_MW_D_01'][0].process_request)
for i in m.methods['test_fun_common']:
    pass
   # print(i.__name__)
#print(m.methods['Test_MW_D_01'][0].__class__.__name__)
print(m.methods["process_request"])
r = m.download(func_test,"requset","spider")

cls = _get_spider_loader(s)

for name, module in cls._spiders.items():
    print(name)
    crawler = Crawler(module,s)
    d = Downloader(crawler)

'''