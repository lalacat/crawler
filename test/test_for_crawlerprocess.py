import warnings
class CrawlerRun(object):



    def __init__(self):
        self.temp_set = set("qwertyuiop")

    @property
    def test1(self):
        #warnings.warn('仅用于提示，而不中断执行')
        return "get_func()"

    name = property(lambda self:self.temp_set,doc="test")

cr = CrawlerRun()
a = cr.temp_set.add()
print(cr.test1)