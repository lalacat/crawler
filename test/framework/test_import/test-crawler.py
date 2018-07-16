from twisted.internet.defer import inlineCallbacks
import logging
from test.framework.test_import.test_loadobject import load_object
from zope.interface.verify import verifyClass,DoesNotImplement
from test.framework.test_import.interface import ISpiderLoader
from zope.interface import Interface
from test.framework.test_spider_framework import ExecutionEngine,MongoDb

logger = logging.getLogger(__name__)

class Crawler(object):

    def __init__(self,spidercls):
        self.crawling = False
        self.spider = None
        self.engine = None
        self.spidercls = spidercls

    @inlineCallbacks
    def crwal(self,*args,**kwargs):
        assert not self.crawling, "已经开始爬虫了........"
        self.crawling = True

        try:
            self.spider = self._create_engine(*args, **kwargs)

    """
    用户封装调度器以及引擎的...
    """
    def _create_engine(self):
        logger.info("爬虫引擎已创建")
        return ExecutionEngine()

    def _create_spider(self,*args, **kwargs):
        logger.info("爬虫： 已创建" )
        return spidercls

    def _create_db(self,db_url,db_name):
        logger.info("数据库已创建")
        return MongoDb(db_url,db_name)


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

