import pymongo
import logging


logger = logging.getLogger(__name__)
class MongoDB(object):

    def __init__(self,settings):
        self.mongo_url = settings["MONGODB_URL"]
        self.db_name = settings["MONGODB_NAME"]
        self.collection_name = None

        try:
            self.client = pymongo.MongoClient(self.db_url)
            self.db = self.client[self.db_name]
        except Exception as e:
            logger.error(e)

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_item(self,item,spider):
        logger.info("添加入数据库")
        _collection = spider.collection
        _db_collection = self.db[_collection]
        if not self._db_collection:
            raise ValueError('没有发现表明%s'%_collection)

        _db_collection.insert_one(item)
        return None
