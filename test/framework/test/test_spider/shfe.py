import json
import re
from collections import defaultdict

import jsonpath
from lxml import etree

from spider import Spider
import logging
from twisted.internet import defer, reactor

from test.framework.core.crawler import Crawler
from test.framework.https.request import Request
from test.framework.crawlRunner.crawlerRunner__for_distribute_from import CrawlerRunner
from test.framework.setting import Setting
from test.framework.test.test_spider.simple_spider.simple_spider_07_mutil_crawlrunner import SimpleSpider_07
logger = logging.getLogger(__name__)

class SHFE_Rank(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    name = "cffex"

    deal_sorts = {
        '0':'total',
        '1':'buy',
        '2':'sale'
    }
    def __init__(self):

        self.total_sale_1810 = 0
        self.total_sale_1811 = 0
        self.total_sale_1812 = 0
        self.total_sale_1903 = 0
        self.total_sale_1906 = 0

        self.instrument_cu = 'cu\d+'
        self.instrument_al = 'al\d+'
        self.instrument_zn = 'zn\d+'
        self.instrument_pb = 'pb\d+'
        self.instrument_ni = 'ni\d+'
        self.instrument_sn = 'sn\d+'
        self.instrument_au = 'au\d+'
        self.instrument_ag = 'ag\d+'
        self.instrument_rb = 'rb\d+'
        self.instrument_hc = 'hc\d+'
        self.instrument_fu = 'fu\d+'
        self.instrument_bu = 'bu\d+'
        self.instrument_ru = 'ru\d+'

    def start_requests(self):
        self.start_urls = [
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181008.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181009.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181010.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181011.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181012.dat',

        'http://www.shfe.com.cn/data/dailydata/kx/pm20181015.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181016.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181017.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181018.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181019.dat',

        'http://www.shfe.com.cn/data/dailydata/kx/pm20181022.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181023.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181024.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181025.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181026.dat',

        'http://www.shfe.com.cn/data/dailydata/kx/pm20181029.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181030.dat',
        'http://www.shfe.com.cn/data/dailydata/kx/pm20181031.dat'

        ]

        for url in self.start_urls:
            yield Request(url, callback=self._parse)

    def _parse(self,response):
        data = json.loads(response.body)
        time = re.findall('\d{4}\d{1,2}\d{1,2}',response.url)
        print(time)

        # express = '$.o_cursor[*]'
        # allitems = jsonpath.jsonpath(data, express)
        #
        # for oneitem in allitems:
        #     if oneitem['PARTICIPANTABBR1'].strip() == '华泰期货':
        #         # 持仓量
        #         volume = oneitem['CJ1']
        #         # print(volume)
        #         # 排名
        #         rank = oneitem['RANK']
        #         # print(rank)
        #         # 合约
        #         instrumen = oneitem['INSTRUMENTID'].strip()
        #         if re.match(self.instrument_cu, instrumen):
        #             print('true')
        #         # print(instrumen)
        #
        #         print(instrumen + ':\t' + str(rank) + ':\t' + str(volume)+'\n')
        return None



if __name__ == '__main__':
    settings = Setting()
    crawler_01 = Crawler(SHFE_Rank, settings)
    c1 = crawler_01.crawl()
    c1.addBoth(lambda _: reactor.stop())
    reactor.run()
