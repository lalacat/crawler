import pprint


class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):

        try:
            print(pprint.pformat(spider.total_result))
        except Exception as e :
            print(e)

        return None