class Test_MW_B(object):
    component_name = "Test_MW_B"

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


def test_fun_B(test):
    print(test)