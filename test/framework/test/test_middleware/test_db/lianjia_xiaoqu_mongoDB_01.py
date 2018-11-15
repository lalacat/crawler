import pymongo
import logging


logger = logging.getLogger(__name__)

class LJ_XQ_DB(object):

    def __init__(self,crawler):
        self.lfm = crawler.logformatter
        logger.debug(*self.lfm.crawled(
            'Pipe',self.__class__.__name__,
            '已初始化...'
        ))
        self.settings = crawler.settings
        self.db_url = self.settings["MONGODB_URL"]
        self.db_name = self.settings["MONGODB_NAME"]
        self.collection_name = None

        try:
            self.client = pymongo.MongoClient(self.db_url)
            self.db = self.client[self.db_name]
        except Exception as e:
            logger.error(*self.lfm.error("Pipe",self.__class__.__name__,
                                         '',
                          '出现错误:'),
             extra=
             {
                 'exception':e,
             })

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def open_spider(self,spider):
        print('mongodb open_spider')
        self.collection_name = spider.name

    def process_item(self,item,spider):
        if not hasattr(spider,"handler_db"):
            logger.debug(*self.lfm.crawled(
                "Spider",spider.name,
                "没有设置数据库操作标志<handler_db>",
                'self.__class__.__name__'))
            return item
        else:
            logger.debug(*self.lfm.crawled(
                "Spider",spider.name,
            '正在添加进入数据库'))

            _db_collection = self.db[self.collection_name]
            # if not _db_collection.find({"total_zone_name":item["total_zone_name"]}).count():
            _db_collection.insert_one(item)
            return None
