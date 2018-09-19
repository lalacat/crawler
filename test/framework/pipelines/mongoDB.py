import pymongo
import logging


logger = logging.getLogger(__name__)

class MongoDB(object):

    def __init__(self,settings):
        self.db_url = settings["MONGODB_URL"]
        self.db_name = settings["MONGODB_NAME"]
        self.collection_name = None

        try:
            self.client = pymongo.MongoClient(self.db_url)
            self.db = self.client[self.db_name]
        except Exception as e:
            logger.error(e)

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_item(self,item,spider):
        assert hasattr(spider,"handler_db"),"Spider(%s)没有设置数据库操作标志<handler_db>"
        if not spider.handler_db:
            return
        logger.debug("添加入数据库")
        try:
            _collection = spider.collection
            _db_collection = self.db[_collection]
        except Exception as e  :
            raise AttributeError('在Spider(%s)没有发现表名属性<colletction>'%(spider.name))
        if not _db_collection.find({"part_zone_name":item["part_zone_name"]}).count():

            _db_collection.insert_one(item)
        return None
