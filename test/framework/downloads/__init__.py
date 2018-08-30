import pprint

from twisted.internet import defer, task

from test.framework.crawler import Crawler, _get_spider_loader
from test.framework.https.request import Request
from test.framework.https.response import Response
from test.framework.middleware import MiddlewareManager
from test.framework.objectimport import bulid_component_list
from test.framework.setting import Setting
from test.framework.objectimport.loadobject import load_object
from test.framework.downloads.download_agent import HTTPDownloadHandler
from test.framework.twisted.defer import mustbe_deferred


class Slot(object):

    def __init__(self,concurrency,delay,randomize_delay):
        pass


class Downloader(object):
    def __init__(self,crawler):
        self.settings = crawler.settings
        self.handler = load_object(self.settings["DOWNLOAD_HANDLER"])
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
        def _deactivate(response):
            self.active.remove(request)
            return response

        self.active.add(request)
        #  调用中间件管理器的download方法，同时传入了自己的_enqueue_request方法。
        dfd = self.middleware.download(self._enqueue_request, request, spider)
        return dfd.addBoth(_deactivate)




class DownloaderMiddlewareManager(MiddlewareManager):

    component_name = 'downloader middleware'
    @classmethod
    def _get_mwlist_from_settings(cls,settings):
        return bulid_component_list(settings['TEST_DOWNLOADER_MIDDLEWARE'])

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

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
            for method in self.methods['process_request']:
                response = yield method(request=request,spider =spider)
                assert response is None or isinstance(response,(Response,Request)),\
                '中间件%s.process_request 执行后返回的数据类型必须是 None,Response或者Request'\
                % method._class__._name__
                #  如果结果是下载后的，就直接返回
                if response:
                    defer.returnValue(response)
            #  如果参数是经过一系列中间件处理过的request，这一步就是对requset进行下载
            defer.returnValue((yield download_func(request=request,spider=spider)))

        @defer.inlineCallbacks
        def process_response(response):
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

        deferred = mustbe_deferred(process_request, request)
        deferred.addErrback(process_exception)
        deferred.addCallback(process_response)
        return deferred


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

'''
cls = _get_spider_loader(s)

for name, module in cls._spiders.items():
    print(name)
    crawler = Crawler(module,s)
    d = Downloader(crawler)

'''