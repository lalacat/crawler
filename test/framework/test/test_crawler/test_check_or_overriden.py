from test.framework.core.crawler import _get_spider_loader
from test.framework.setting import Setting,overridden_or_new_settings
import logging
logging.basicConfig(level=logging.DEBUG)

s = Setting()

_active = set()
new_s = s.copy()
cls = _get_spider_loader(new_s)

new_and_over_setting = ["TEST2 = t2","TEST3 = t3"]

temp = [ x.split('=',1)for x in new_and_over_setting]

tm= dict(temp)

for k,v in tm.items():
    new_s.set(k.strip(),v,"project")

d = dict(overridden_or_new_settings(new_s))



logging.info("Overridden settings:\n %(settings)r", {'settings': d})

'''



for name, module in cls._spiders.items():
    module.update_settings(new_s)
    overridden_or_new_settings(new_s)

'''
