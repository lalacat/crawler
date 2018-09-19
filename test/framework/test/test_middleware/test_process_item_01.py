
class Test_Process_item_A(object):

    def __init__(self,crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    '''
    def process_item(self,item,spider):
        print("process  item")
        item["test"] = "test"
        return item
    '''