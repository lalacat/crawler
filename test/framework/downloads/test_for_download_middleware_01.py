import logging

import six


class Test_MW_D_01(object):
    component_name = "Test_MW_D_01"

    def __init__(self,crawler):
        self.crawler = crawler

    def process_request(self,request,spider):
        if spider.name == "test1":
            logging.info("mw_d_01 inner test")
            request.meta["test1"] = "Test_MW_D_01"
        return

    def open_spider(self):
        print("mw_d_01 inner test")
        return

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_D_A(test):
    print(test)

def test_fun_common(test):
    print("mw_d_01",test)
    return "from mw_d_01"



assert 5>7, logging.info("False")