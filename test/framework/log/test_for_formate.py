import os,logging
from test.framework.test_import.loadobject import load_object
from test.framework.setting import Setting

class A(object):

    def __init__(self):
        self.flags = "Test"
        self.name ="name"
        self.status = "500"

rq= A()
rp= A()
sp= A()
s = Setting()
lf = load_object(s['LOG_FORMATTER'])
logfor = lf.from_crawler(rq)
strs = logfor.crawled(rq,rp,sp)
print(strs)