from test.framework.setting import Setting
from test.framework.core.crawler import Crawler
from twisted.internet import reactor
from framework.test import Cffex_Rank

'''
LOG_FORMAT = '[%(levelname)s] [%(asctime)s]-[%(filename)s][line:%(lineno)d]: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)
'''




settings = Setting()
crawler_01 = Crawler(Cffex_Rank,settings)
c1 = crawler_01.crawl()
c1.addBoth(lambda _:reactor.stop())
reactor.run()

