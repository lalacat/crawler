class Test_MW_C(object):
    component_name = "Test_MW_C"

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

def test_fun_C(test):
    print(test)

def test_fun_common(test):
    print("mw_03",test)
    return "from mw_03"