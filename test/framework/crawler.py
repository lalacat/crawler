from twisted.internet.defer import inlineCallbacks,maybeDeferred
import logging
from test.framework.test_import.test_loadobject import load_object
from zope.interface.verify import verifyClass,DoesNotImplement
from test.framework.interface import ISpiderLoader
from test.framework.test_spider_framework import ExecutionEngine,MongoDb

logger = logging.getLogger(__name__)


class Crawler(object):
    # 将编写的爬虫类包装成可可以进行工作的爬虫，
    # 装载爬虫，导入爬虫的网页
    # 将爬虫导入到引擎中
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
            self.spider = self._create_spider(*args, **kwargs)
            self.engine = self._create_engine()
            start_requests = iter(self.spider.start_requests())
            yield self.engine.open_spider(self.spider,start_requests)
            '''
            此函数的功能就是如果作为其参数返回值为defer，那么其不作任何处理，原样将defer返回。
            但如何返回值不是defer而是一个值（正如我们的缓存代理将本地缓冲的诗歌返回一样），那么这个maybeDeferred会将该值重新打包成一个已经激活的deferred返回，注意是已经激活的deferred。
            当然，如果返回的是一个异常，其也会将其打包成一个已经激活的deferred，只不过就不是通过callback而是errback激活的。
            '''
            yield maybeDeferred(self.engine.start)
        except Exception:
            self.crawling = False
            if self.engine is not None:
                yield self.engine.close()

            raise


    """
    用户封装调度器以及引擎的...
    """
    def _create_engine(self):
        logger.info("爬虫引擎已创建")
        return ExecutionEngine(self,lambda _: self.stop())

    def _create_spider(self,*args, **kwargs):
        logger.info("爬虫：%s 已创建" %self.spidercls.name)
        return self.spidercls.from_crawler(self,*args,**kwargs)

    def _create_db(self,db_url,db_name):
        logger.info("数据库已创建")
        return MongoDb(db_url,db_name)


    @inlineCallbacks
    def stop(self):
        if self.crawling:
            self.crawling = False
            yield maybeDeferred(self.engine.stop)






class CrawlerRunner(object):
    def __init__(self):
        self.spider



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
