class Test_MW_D_02(object):
    component_name = "Test_MW_D_02"

    def __init__(self,crawler):
        self.crawler = crawler

    def process_request(self):
        print("mw_d_02inner test")
        return "from mw_d_02"

    def open_spider(self):
        print("mw_d_02 inner test")
        return "from mw_d_02"

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_D_B(test):
    print(test)

def test_fun_common(test):
    print("mw_d_02",test)
    return "from mw_d_02"