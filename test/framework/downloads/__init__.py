import random
import warnings
import logging
from collections import deque
import time

from twisted.internet import defer, task,reactor

from test.framework.middleware.downloadmw import DownloaderMiddlewareManager
from test.framework.objectimport.loadobject import load_object
from test.framework.utils.defer import mustbe_deferred
from test.framework.utils.httpobj import urlparse_cached

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
        #  给一个随机时间
        if self.randomize_delay:
            #  生成下一个实数，它在 [x, y) 范围内
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
                len(self.active), len(self.queue), len(self.transferring),self.lastseen)
            )


#  延迟，通过spider设置延迟
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
        self.spider = None
        self.slots = {}
        # active是一个活动集合，用于记录当前正在下载的request集合。
        self.active = set()
        # 从配置中获取设置的并发数
        self.total_concurrency = self.settings.getint('CONCURRENT_REQUESTS')
        # 同一域名并发数
        self.domain_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        # 同一IP并发数
        self.ip_concurrency = self.settings.getint('CONCURRENT_REQUESTS_PER_IP')
        # 随机延迟下载时间 默认是True
        self.randomize_delay = self.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        # 初始化下载器中间件
        self.middleware = DownloaderMiddlewareManager.from_crawler(crawler)
        # ask.LoopingCall安装了一个60s的定时心跳函数_slot_gc,这个函数用于对slots中的对象进行定期的回收。
        self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        self._slot_gc_loop.start(60)

    #  进行加载中间件，及对requset进行下载
    def fetch(self,request,spider):
        logger.debug("加载中间件，准备下载")
        self.spider = spider

        def _deactivate(response):
            self.active.remove(request)
            return response

        self.active.add(request)
        #  调用中间件管理器的download方法，同时传入了自己的_enqueue_request方法。
        dfd = self.middleware.download(self._enqueue_request, request,spider)
        #dfd = self.middleware.download(self._download, request, spider)
        return dfd.addBoth(_deactivate)

    def needs_backout(self):
        #  进行的下载任务的个数大于等于并发数，默认并发数为16，表示下载要延缓一下
        if len(self.active) >= self.total_concurrency:
            logger.warning("%s 的下载数超过最大同时下载数%d"%(self.spider.name,self.total_concurrency))
            return True
        return False

    def _get_slot(self, request, spider):
        #  通过slots集合达到了缓存的目的，对于同一个域名的访问策略可以通过slots获取而不用每次都解析配置。
        #  然后根据key从slots里取对应的Slot对象，如果还没有，则构造一个新的对象。
        key = self._get_slot_key(request, spider)
        if key not in self.slots:
            #  ip_concurrency默认为0，domain_concurrency默认为8，
            conc = self.ip_concurrency if self.ip_concurrency else self.domain_concurrency
            #  用spider中的设置来改变默认的conc，delay
            conc, delay = _get_concurrency_delay(conc, spider, self.settings)
            self.slots[key] = Slot(conc, delay, self.randomize_delay)

        return key, self.slots[key]

    def _get_slot_key(self, request, spider):
        #  request对应的域名也增加了缓存机制:urlparse_cached,dnscahe.
        if 'download_slot' in request.meta:
            return request.meta['download_slot']
        #  判断hostname在缓存中是否存在
        key = urlparse_cached(request).hostname or ''
        ''' 
        if self.ip_concurrency:
            key = dnscache.get(key, key)
        '''
        return key

    #  处理requset
    def _enqueue_request(self, request, spider):
        #  key就是hostname
        logger.info("%s.%s加入download队列，加入时间为%f"%(spider.name,request,time.clock()))
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
        now = time.clock()
        delay = slot.download_delay()  # 获取slot对象的延迟时间
        if delay:
            #  delay在默认情况下为0
            penalty = delay + slot.lastseen - now  # 距离上次运行还需要延迟则latercall
            if penalty > 0:
                slot.latercall = reactor.callLater(penalty, self._process_queue, spider, slot)
                return

        # Process enqueued requests if there are free slots to transfer for this slot
        while slot.queue and slot.free_transfer_slots() > 0:
            logger.debug(len(slot.queue))
            # 不停地处理slot队列queue中的请求，如果队列非空且slot.transferring中request的个数没有达到下载最大个数,
            # 则下载，如果需要延迟则继续调用'_process_queue'
            slot.lastseen = now
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)
            # prevent burst if inter-request delays were configured
            if delay:
                self._process_queue(spider, slot)
                break

    def _download(self,slot,request, spider):
        logger.debug("进行下载。。。。。")
        #logger.info("request：%s，spider: %s"%(request,spider))
        try:
            dfd = mustbe_deferred(self.handler.download_request,request,spider)
        except Exception:
            raise ValueError("can't find spider")

        slot.transferring.add(request)

        def finish_transferring(_):
            slot.transferring.remove(request)
            self._process_queue(spider, slot)
            return _

        return dfd.addBoth(finish_transferring)
        #return dfd

    def close(self):
        logger.info("关闭 %s 的下载器"%self.spider.name)
        self._slot_gc_loop.stop()
        ''' 
        for slot in iter(self.slots):
            slot.close()
        '''


    #  垃圾回收
    def _slot_gc(self, age=60):
        """
        如果一个Slot对象没有正在活动的下载request,且距离上次活动的时间已经过去了60s则进行回收。
        :param age:
        :return:
        """
        mintime = time.clock() - age
        for key, slot in list(self.slots.items()):
            if not slot.active and slot.lastseen + slot.delay < mintime:
                self.slots.pop(key).close()


