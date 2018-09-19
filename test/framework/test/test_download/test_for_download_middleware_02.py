import logging


class Test_MW_D_02(object):
    component_name = "Test_MW_D_02"

    def __init__(self,crawler):
        self.crawler = crawler

    def process_request(self,request,spider):
        if spider.name == "test2":
            logging.info("mw_d_02 inner test")
            request.meta["test2"] = "Test_MW_D_02"
        return

    def open_spider(self):
        print("mw_d_02 inner test")
        return

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_D_B(test):
    print(test)

def test_fun_common(test):
    print("mw_d_02",test)
    return "from mw_d_02"