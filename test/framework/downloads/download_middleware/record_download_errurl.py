import logging

from twisted.python.failure import Failure

logger = logging.getLogger(__name__)


class RecordDownloadErrorUrl(object):

    def __init__(self,crawler):
        self.lfm = crawler.logformatter
        logger.info(*self.lfm.crawled(
            "DownloadMiddleware",self.__class__.__name__,
            '已初始化！！'
        ))
        self._settings = crawler.settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_exception(self,request,exception,spider):
        proxy = request.meta.get('proxy',None)

        # logger.error(exception)
        _failure = exception.value
        logger.error(*self.lfm.error(
            "Request",request,
            _failure,
            {
                'function':proxy
            }
        ))
        return None

