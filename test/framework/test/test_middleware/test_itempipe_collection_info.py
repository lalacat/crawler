

class Collection_print(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)


    def process_item(self,item,spider):
        print(len(item))
        return None
