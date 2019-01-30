import json
import pprint
import re
import logging

from collections import defaultdict
from lxml import etree
from twisted.internet import defer

from test.framework.spider import Spider
from test.framework.https.request import Request
from test.framework.core.crawlerRunner import CrawlerRunner
from test.framework.test.test_example.mutil_sold_info.child_spider_sold_xpath import CollectSold

logger = logging.getLogger(__name__)


class ParentSoldSale(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    def __init__(self):
        self.name = ""
        self._start_urls = []
        self.handler_db = False
        self.change_header = True
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

        #logger.critical("%s的总页数是%d" % (self.name, self.total_page_number))

        for i in range(2,self.total_page_number+1):
        # for i in range(2,3):
            url = self._start_urls[0] + '/pg' + str(i)
            yield Request(url, callback=self._parse_getCommunityInfo,meta={"page_num":i})

    @defer.inlineCallbacks
    def _parse_getCommunityInfo(self,response):
        seletor = etree.HTML(response.body)
        page_num = response.request.meta["page_num"]
        all_communities = seletor.xpath('/html/body/div[4]/div[1]/ul/li')
        self.result[str(page_num)]=self._get_onePage(all_communities)
        for result in self.result[str(page_num)]:
            community_url = result["community_url"]
            name = result['community_name']
            community_name = community_url.split('/')[-2]

            sale_url = re.sub(community_name, 'c' + community_name, re.sub(r'xiaoqu', 'ershoufang', community_url))
            sold_url = re.sub(community_name, 'c' + community_name, re.sub(r'xiaoqu', 'chengjiao', community_url))

            self.sale_url['sale_'+name] = sale_url
            self.sold_url['sold_'+name] = sold_url

        # total_dict = dict(self.sale_url,**self.sold_url)
        # # print(pprint.pformat(total_dict))
        # print(len(total_dict))
        # return None
        try:
            cr = CrawlerRunner(self.sold_url,self.settings,CollectSold,name=self.name,logformat=self.lfm,middlewares=self.crawler.middlewares)
            yield cr.start()
        except Exception as e :
            raise e

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



