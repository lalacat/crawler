import pprint

from twisted.internet import defer

from test.framework.crawler import Crawler, _get_spider_loader
from test.framework.middleware import MiddlewareManager
from test.framework.objectimport import bulid_component_list
from test.framework.setting import Setting
from test.framework.objectimport.loadobject import load_object
from test.framework.downloads.download_agent import HTTPDownloadHandler



class Slot(object):

    def __init__(self,concurrency,delay,randomize_delay):
        pass


class Downloader(object):
    def __init__(self,crawler):
        self.settings = crawler.settings
        self.handler = load_object(self.settings["DOWNLOAD_HANDLER"])



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



s = Setting()

m = DownloaderMiddlewareManager.from_settings(s,"A")

print(m.methods['Test_MW_D_01'][0])

m.methods['test_fun_common'].append(m.methods['Test_MW_D_01'][0].process_request)
for i in m.methods['test_fun_common']:
    print(i.__name__)
print(m.methods['Test_MW_D_01'].__class__.__name__)
print(m.methods['test_fun_common'])

'''
cls = _get_spider_loader(s)

for name, module in cls._spiders.items():
    print(name)
    crawler = Crawler(module,s)
    d = Downloader(crawler)

'''