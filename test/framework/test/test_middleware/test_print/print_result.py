class Print_Result(object):

    def __init__(self,crawler):
        pass

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_item(self,item,spider):
        print(item)