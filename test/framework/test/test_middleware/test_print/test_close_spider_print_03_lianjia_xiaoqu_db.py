
class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        try:
            print("%s 理论获取小区数为%d个"%(spider.name,int(spider.result["total_xiaoqu_number"][0])))

        except Exception as e :
            print("Spider_Out_print",e)

        return None
