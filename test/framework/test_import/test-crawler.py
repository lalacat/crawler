from twisted.internet.defer import inlineCallbacks
import logging
from test.framework.test_import.test_loadobject import load_object
from zope.interface.verify import verifyClass,DoesNotImplement
from test.framework.test_import.interface import ISpiderLoader
from zope.interface import Interface


logger = logging.getLogger(__name__)

class Crawler(Interface):

    def __init__(self):
        self.crawling = False
        pass

    @inlineCallbacks
    def crwal(self,*args,**kwargs):
        assert not self.crawling, "已经开始爬虫了........"
        self.crawling = True



class CrawlerRunner(object):
    pass

class CrawlerProcess(CrawlerRunner):
    def __init__(self):
        super(CrawlerProcess,self).__init__()






def _get_spider_loader():
    cls_path = "test.framework.test_import.spiderloader.SpiderLoader"
    loader_cls = load_object(cls_path)
    try:
        verifyClass(ISpiderLoader,loader_cls)

    except AttributeError as e :
        logger.warning("接口方法实现不完全：",e)

    except DoesNotImplement:
        logger.warning("爬虫导入失败，查看设定是否爬虫爬虫导入类的地址设置"
                       "")

    return loader_cls.from_settings()


cls = _get_spider_loader()

