import logging
import time
from collections import defaultdict

import pymongo
from twisted.internet.error import ConnectionLost

from twisted.python.failure import Failure
from twisted.web._newclient import ResponseNeverReceived

logger = logging.getLogger(__name__)


class RecordDownloadErrorUrl(object):

    def __init__(self,crawler):
        self.lfm = crawler.logformatter
        logger.info(*self.lfm.crawled(
            "DownloadMiddleware",self.__class__.__name__,
            '已初始化！！'
        ))
        self._settings = crawler.settings
        self.MongDB_URl = self._settings['MONGODB_URL']
        self.MongDB_DATABASE = self._settings['MONGODB_NAME_SOLD']
        self.collection_name = 'ErrUrl'

        self.bulid_time = time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
        self.base_date = {'bulid_time': self.bulid_time}
        self.bulid_Flag = True
        self.spider_names = dict()

        try:
            self.client = pymongo.MongoClient(self.MongDB_URl)
            self.db = self.client[self.MongDB_DATABASE]

        except Exception as e:
            raise Exception(e)

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_exception(self,request,exception,spider):
        try:
            if self.bulid_Flag:
                self.bulid_Flag = False
                self.db_coll = self.db[self.collection_name]
                self.db_coll.insert(self.base_date)
                self._id = self.db_coll.find(self.base_date).next()['_id']
            db_msg = dict()
            if self.spider_names.get(spider.name):
                name = spider.name+'_'+str(self.spider_names[spider.name])
            else:
                self.spider_names[spider.name] = 1
                name = spider.name + "_" + str(1)
            _failure = exception.value
            if isinstance(_failure, TimeoutError):
                download_times = request.meta.get('timeout_times')
                if download_times != 4:
                    return None
            elif isinstance(_failure,ResponseNeverReceived):
                logger.error(*self.lfm.error(
                    'Request',request.url,
                    '<ResponseNeverReceived>错误'
                ))
            elif isinstance(_failure,ConnectionLost):
                logger.error(*self.lfm.error(
                    'Request', request.url,
                    '<ConnectionLost>错误'
                ))
            else :
                logger.error(type(_failure))
                raise TypeError('获取的Exception的类型没有包含')

            db_msg[name] = {
                'url': request.url,
                'exception': str(_failure)
            }
            from bson import ObjectId
            self.db_coll.update(
                {'_id': ObjectId(self._id)},
                {'$set': {
                    name:db_msg[name]
                }})
        except Exception as e:
            raise Exception('RecordDownloadErrorUrl %s' %str(e))
        self.spider_names[spider.name] += 1
        return None



