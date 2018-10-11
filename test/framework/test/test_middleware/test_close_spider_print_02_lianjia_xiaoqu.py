import pprint

class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def close_spider(self,spider):
        #print("close_spider")
        try:
            print("%s 理论获取小区数为%d个，实际获得小区数为%d个"
                  %(spider.name,int(spider.result["total_xiaoqu_number"][0]),spider.result_len))
        except Exception as e :
            print(e)
        return None
