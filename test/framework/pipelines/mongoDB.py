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
        logger.debug("添加入数据库")
        try:
            _collection = spider.collection
            _db_collection = self.db[_collection]
        except Exception as e  :
            raise ValueError('没有发现表名%s'%_collection)
        if _db_collection.find({"part_zone_name":item["part_zone_name"]}).count():
            _db_collection.insert_one(item)
        return None
