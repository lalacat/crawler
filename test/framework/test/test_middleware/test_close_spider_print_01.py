class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        print(spider.total_number_community)
        for i, v in spider.part_numbers.items():
            print(i, v)
        return None