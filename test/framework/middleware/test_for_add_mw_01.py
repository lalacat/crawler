class Test_MW_A(object):
    component_name = "Test_MW_A"

    def __init__(self,crawler):
        self.crawler = crawler


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

def test_fun_A(test):
    print(test)