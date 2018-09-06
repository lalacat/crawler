import logging


class Test_MW_D_03(object):
    component_name = "Test_MW_D_03"

    def __init__(self,crawler):
        self.crawler = crawler

    def process_request(self,request,spider):
        if spider.name == "test3":
            logging.info("mw_d_03 inner test")
            request.meta["test3"] = "Test_MW_D_03"
        return

    def open_spider(self):
        print("mw_d_03 inner test")
        return

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_D_C(test):
    print(test)

def test_fun_common(test):
    print("mw_d_03",test)
    return "from mw_d_03"