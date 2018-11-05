
class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        if hasattr(spider,'total_sale_1810'):
            print(spider.total_sale_1810)
        if hasattr(spider,'total_sale_1811'):
            print(spider.total_sale_1811)
        if hasattr(spider,'total_sale_1812'):
            print(spider.total_sale_1812)
        if hasattr(spider,'total_sale_1903'):
            print(spider.total_sale_1903)
        if hasattr(spider,'total_sale_1906'):
            print(spider.total_sale_1906)

        return None
