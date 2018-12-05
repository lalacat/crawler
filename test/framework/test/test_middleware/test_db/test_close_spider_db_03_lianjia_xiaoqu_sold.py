import logging
import pymongo

logger = logging.getLogger(__name__)

class LJ_Sold_DB(object):
    def __init__(self,crawler):
        self.lfm = crawler.logformatter
        logger.debug(*self.lfm.crawled(
            'Pipe',self.__class__.__name__,
            '已初始化...'
        ))
        self.settings = crawler.settings
        self.db_url = self.settings["MONGODB_URL"]
        self.db_name = self.settings["MONGODB_NAME_SOLD"]
        self.collection_name = None

        self.update_query = None
        self.update_doctument= None
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

    def close_spider(self,spider):
        try:
            if hasattr(spider,'father_name'):
                self.collection_name = spider.father_name
            else:
                return None
            if not hasattr(spider, "sold_db"):
                logger.debug(*self.lfm.crawled(
                    "Spider", spider.name,
                    "没有设置数据库操作标志<handler_db>",
                    'self.__class__.__name__'))
                return None
            else:
                if spider.sold_db:
                    logger.debug(*self.lfm.crawled(
                        "Spider", spider.name,
                        '正在添加进入数据库'))
                    item = dict()
                    item['community_name'] = spider.name
                    item.update(spider.result)
                    self._db_collection = self.db[self.collection_name]
                    if self.db_filter(item) == 'insert':
                        self._db_collection.insert_one(item)
                    # elif self.db_filter(item) == 'update':
                    #     self._db_collection.update(self.update_query, self.update_doctument)
                    return None
                return None
        except Exception as e :
            print(e)
        self.db.logout()

    def db_filter(self,item):
        #  1.防止重复写入
        #  2.对某条字段更新
        if self._db_collection.find(item).count() >= 1:
            #  爬到的对象未更新
            return 'exist'
        elif self._db_collection.find({'community_name':item['community_name']}).count() >= 1:
            self.update_query = {'community_name':item['community_name']}
            new_house = dict()
            self.update_doctument ={'$set':{
                   'community_sale_num': item['community_sale_num'],
                   'community_rent_num': item['community_rent_num'],
                   'community_onsale_num': item['community_onsale_num'],
                   'community_avr_price': item['community_avr_price']
                }}
            return 'update'
        else:
            # self._db_collection.find(item).count() == 0:
            return 'insert'
        # else:
        #     print('Nothing')
        #     'Nothing'

