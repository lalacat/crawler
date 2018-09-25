import pprint

class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        #print(pprint.pformat(spider.all_zones))
        for i, v in spider.all_zones.items():
            print(i, v)

        for i in spider.all_towns:
            print(i)

        return None
