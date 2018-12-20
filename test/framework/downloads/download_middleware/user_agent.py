import logging
import random

from twisted.web.http_headers import Headers

logger = logging.getLogger(__name__)


class Change_Request_UserAgent(object):

    def __init__(self,crawler):
        self.lfm = crawler.logformatter
        logger.info(*self.lfm.crawled(
            "DownloadMidder",self.__class__.__name__,
            '已初始化！！'
        ))
        self._settings = crawler.settings
        self._headers = self._settings["HEADER_COLLECTION"]
        self.used_header = set()


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        # TODO 修改Header值得修改方式
        if request.meta.get('header_flag'):
            if request.meta['header_flag']:
                if request.meta.get('last_header'):
                    last_header = request.meta['last_header']
                    new_header = Headers({'User-Agent':random.choice(self._headers)})
                    while new_header == last_header:
                        new_header = Headers({'User-Agent':random.choice(self._headers)})
                        # self.used_header.add(new_header)
        else:
            new_header = Headers({'User-Agent':random.choice(self._headers)})
            # self.used_header.add(new_header)
        request.headers = new_header
        return None

    def _set_user_agent(self,name = 'User-Agent',value = None):
        if