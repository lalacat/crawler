import json
import pprint
import re
from collections import defaultdict

from lxml import etree
from twisted.internet import defer

from spider import  Spider
import logging

from test.framework.https.request import Request
from test.framework.test.test_crawlerRunner.crawlerRunner_for_distribute_from_01 import CrawlerRunner
from test.framework.test.test_spider.lianjia_spider.lianjia_spider_onsale_sold_01 import SoldOrSale

logger = logging.getLogger(__name__)

class SimpleSpider_08(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    def __init__(self):
        self.name = ""
        self._start_urls = []
        self.handler_db = False
        self.total_number_community = 0
        self.result = defaultdict(list)
        self.result_len = 0
        self.sale_url = dict()
        self.sold_url = dict()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, info):
        base_name = "Task_"
        self._name = base_name+info

    @property
    def start_urls(self):

        return self._start_urls

    @start_urls.setter
    def start_urls(self,urls):
        if not isinstance(urls,list):
            self._start_urls = [urls]
        else:
            self._start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self._parse_getAllCommunity)

    def _parse_getAllCommunity(self,response):
        seletor = etree.HTML(response.body)
        #  获取下属城镇的小区总页数
        page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        self.total_page_number = json.loads(page_number[0])["totalPage"]
        total_xiaoqu_number = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
        self.result["total_xiaoqu_number"] = [total_xiaoqu_number]
        logger.critical("%s的总页数是%d" % (self.name, self.total_page_number))

        # for i in range(1, self.total_page_number+1):
        for i in range(1, 2):
            url = self._start_urls[0] + '/pg' + str(i)
            yield Request(url, callback=self._parse_getCommunityInfo,meta={"page_num":i})

    @defer.inlineCallbacks
    def _parse_getCommunityInfo(self,response):
        seletor = etree.HTML(response.body)
        page_num = response.requset.meta["page_num"]
        all_communities = seletor.xpath('/html/body/div[4]/div[1]/ul/li')
        self.result[str(page_num)]=self._get_onePage(all_communities)
        self.result_len += len(self.result[str(page_num)])
        # print(self.name+':'+str(page_num)+"============================")
        for result in self.result[str(page_num)]:
            community_url = result["community_url"]
            name = result['community_name']
            community_name = community_url.split('/')[-2]

            sale_url = re.sub(community_name, 'c' + community_name, re.sub(r'xiaoqu', 'ershoufang', community_url))
            sold_url = re.sub(community_name, 'c' + community_name, re.sub(r'xiaoqu', 'chengjiao', community_url))

            self.sale_url[name] = sale_url
            self.sold_url[name] = sold_url

        print(pprint.pformat(self.sale_url))
        print(pprint.pformat(self.sold_url))
        # self.sale_url['']
        # urls = {
        #     'sale':on_sale_url,
        #     'sold':had_saled_url,
        # }
        try:
            cr = CrawlerRunner(self.sale_url,self.settings,SoldOrSale)
            yield cr.start()
        except Exception as e :
            print(e)
        return None


    def _get_onePage(self,all_communities):
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



