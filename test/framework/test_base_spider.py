
from test.framework.utils.record_live_instances import object_ref
import logging



class Spider(object_ref):
    name = None
    def __init__(self,name=None,**kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self,"name",None):
            raise ValueError("自定义的%s 必须有个名字name" %type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self,'start_urls'):
            self.start_urls = []
    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        #使用LoggerAdapter类来传递上下文信息到日志事件的信息中
        return logging.LoggerAdapter(logger,{"爬虫":self})

    @classmethod
    def from_crawler(cls,crawler,*args,**kwargs):
        spider = cls(*args,**kwargs)
        spider._ser_crawler(crawler)
        return spider

    def _ser_crawler(self,crawler):
        self.crawler = crawler

