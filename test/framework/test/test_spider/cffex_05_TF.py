from lxml import etree

from test.framework.spider import Spider
import logging
from twisted.internet import reactor

from test.framework.core.crawler import Crawler
from test.framework.https.request import Request
from test.framework.setting import Setting

logger = logging.getLogger(__name__)

class Cffex_Rank(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    name = "cffex_TF"

    deal_sorts = {
        '0':'total',
        '1':'buy',
        '2':'sale'
    }
    def __init__(self):

        self.total_sale_1812 = 0
        self.total_sale_1903 = 0
        self.total_sale_1906 = 0


    def start_requests(self):

        self.start_urls = [
        'http://www.cffex.com.cn/sj/ccpm/201810/08/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/09/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/10/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/11/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/12/TF.xml',

        'http://www.cffex.com.cn/sj/ccpm/201810/15/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/16/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/17/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/18/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/19/TF.xml',

        'http://www.cffex.com.cn/sj/ccpm/201810/22/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/23/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/24/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/25/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/26/TF.xml',

        'http://www.cffex.com.cn/sj/ccpm/201810/29/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/30/TF.xml',
        'http://www.cffex.com.cn/sj/ccpm/201810/31/TF.xml'

        ]

        for url in self.start_urls:
            yield Request(url, callback=self._parse)

    def _parse(self,response):
        # print(response.body)
        seletor = etree.HTML(response.body)
        # company = seletor.findall('data ')
        # print(len(company))
        for item in seletor.iter('data'):
            if item.find('shortname').text == '华泰期货':

                data_list = item.xpath('@*')
                # 成交种类
                data_value = self.deal_sorts[data_list[0]]
                # 成交合约
                data_Text  = data_list[1].strip()
                # 成交日期
                tradingday = item.find('tradingday').text
                # 成交量
                volume = item.find('volume').text
                if data_value == 'total':
                    if data_Text == 'TF1812':
                        print(data_Text+":"+volume)
                        self.total_sale_1812 += int(volume)

                    if data_Text == 'TF1903':
                        # print(data_Text+":"+volume)
                        self.total_sale_1903 += int(volume)

                    if data_Text == 'TF1906':
                        # print(data_Text+":"+volume)
                        self.total_sale_1906 += int(volume)


        return None



if __name__ == '__main__':
    settings = Setting()
    crawler_01 = Crawler(Cffex_Rank, settings)
    c1 = crawler_01.crawl()
    c1.addBoth(lambda _: reactor.stop())
    reactor.run()
