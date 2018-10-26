import json
from collections import defaultdict

from lxml import etree

from spider import Spider
import logging
from twisted.internet import defer

from test.framework.https.request import Request
from test.framework.crawlRunner.crawlerRunner__for_distribute_from import CrawlerRunner
from test.framework.test.test_spider.simple_spider.simple_spider_07_mutil_crawlrunner import SimpleSpider_07
logger = logging.getLogger(__name__)

class SimpleSpider_06(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    name = "caolu"
    def __init__(self):
        self.handler_db = True
        self.total_number_community = 0
        self.result = defaultdict(list)
        self.result_len = 0

    def start_requests(self):
        self.start_urls = [
            #"https://sh.lianjia.com/xiaoqu/biyun/",
            "https://sh.lianjia.com/xiaoqu/caolu/"
        ]
        for url in self.start_urls:
            yield Request(url, callback=self._parse)

    @defer.inlineCallbacks
    def _parse(self,response):
        seletor = etree.HTML(response.body)
        #  获取下属城镇的小区总页数
        page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        self.total_page_number = json.loads(page_number[0])["totalPage"]
        total_xiaoqu_number = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
        logger.debug("%s的总页数是%d" % (self.name, self.total_page_number))
        self.result["total_xiaoqu_number"] = [total_xiaoqu_number]
        '''
        urls = list()
        for i in range(1, self.total_page_number + 1):
            url = response.requset.url + 'pg' + str(i)
            urls.append(url)
        '''

        # urls = [
        #     'https://sh.lianjia.com/xiaoqu/anshan/',  # 157 156
        #     'https://sh.lianjia.com/xiaoqu/dongwaitan/',# 144 141
        # ]
        # try:
        #     cr = CrawlerRunner.task_from(urls,SimpleSpider_07)
        #     #cr.start()
        #     #d.addBoth(lambda _: print(_))
        #     yield cr.start()
        # except Exception as e :
        #     print(e)
        return None

        #url = response.requset.url + 'pg' + str(2)
        #yield Request(url, callback=self._parse2,meta={"page_num":2})


    """
    def _parse2(self,response):
        seletor = etree.HTML(response.body)
        page_num = response.requset.meta["page_num"]
        all_communities = seletor.xpath('/html/body/div[4]/div[1]/ul/li')
        self.result[str(page_num)]=self.get_onePage(all_communities)
        self.result_len += len(self.result[str(page_num)])

        return None
        #return self.result[str(page_num)]

    def get_onePage(self,all_communities):
        one_page = list()
        for community in all_communities:
            result = dict()
            # 小区总信息
            community_info = community.xpath('./div[@class="info"]')[0]

            # 小区名称
            community_name = community_info.xpath('./div[@class="title"]/a')[0].text
            result["community_name"] = community_name

            # 小区url
            community_url = community_info.xpath('./div[@class="title"]/a')[0].get('href')
            result["community_url"] = community_url

            # 小区房屋信息
            community_sale_num = community_info.xpath('./div[@class="houseInfo"]/a[1]')[0].text
            community_rent_num = community_info.xpath('./div[@class="houseInfo"]/a[2]')[0].text
            community_onsale_num = community_info.xpath('../div[@class="xiaoquListItemRight"]/div[2]/a/span/text()')[0]

            result["community_sale_num"] = re.findall('\d+', community_sale_num)[1]
            result["community_rent_num"] = re.findall('\d+', community_rent_num)[0]
            result["community_onsale_num"] = community_onsale_num

            # 小区年限
            community_bulid_year = community_info.xpath('./div[@class="positionInfo"]/text()')[3].replace('/',"").strip()
            '''
            if str(community_bulid_year) == '未知年建成':
                print(community_bulid_year)
            else:
                print(community_bulid_year, re.findall('\d+', community_bulid_year)[0])
            '''
            result["community_bulid_year"] = community_bulid_year

            # 小区均价
            community_avr_price = community_info.xpath('../div[@class="xiaoquListItemRight"]/div/div/span/text()')[0]
            result["community_avr_price"] = community_avr_price
            one_page.append(result)

        return one_page
        """
