class Test_MW_D_03(object):
    component_name = "Test_MW_D_03"

    def __init__(self,crawler):
        self.crawler = crawler


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_D_C(test):
    print(test)

def test_fun_common(test):
    print("mw_d_03",test)
    return "from mw_d_03"