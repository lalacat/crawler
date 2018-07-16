
from test.framework.test_import.record_live_instances import object_ref
from test.framework.test_import.record_live_instances import print_live_refs




class Spider(object_ref):

    def __init__(self):
        self.test = "a"




class child_Spider(Spider):
    def __int__(self):
        self.test = "child Spider"
class child_Spider1(Spider):
    def __int__(self):
        self.test = "child Spider"
class child_Spider2(Spider):
    def __int__(self):
        self.test = "child Spider"

s = Spider()
c = child_Spider()
c1 = child_Spider1()
c2 = child_Spider2()
c3 = child_Spider()
x = Spider()
print_live_refs(Spider)