import json
from collections import defaultdict
from urllib.parse import urljoin, urlparse, urlunparse

from lxml import etree

from spider import Spider
from test.framework.https.request import Request


class SoldOrSale(Spider):
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
            if self.name.split('_')[-1] == 'sale':
                yield Request(url,callback=self._parse_sale)
            else:
                yield Request(url,callback=self._parse_sold)


    def _parse_sale(self,response):
        seletor = etree.HTML(response.body)
        # 所有的在售房屋列表
        houses = seletor.xpath("//ul[@class='sellListContent']")[0].xpath('./li')

        print(len(houses))

        # 总的套数
        total_num = seletor.xpath('//div/h2[@class="total f1"]/span/text()')

        for on_house in houses:
            # 总价及均价
            total_price_xpath = on_house.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice']/span")
            # total_price = total_price_xpath[0].text if total_price_xpath else None
            total_price = self._xpath_filter(total_price_xpath)

            unit_prince_xpath = on_house.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span")
            unit_prince = unit_prince_xpath[0].text
            print(total_price)
            print(unit_prince)

            # 小区名称及网址
            title = on_house.xpath("./div[@class='info clear']/div[@class='title']/a")[0].text
            title_url = on_house.xpath("./div[@class='info clear']/div[@class='title']/a/@href")[0]
            print(title)
            print(title_url)

            # 小区地址
            address = on_house.xpath("./div[@class='info clear']/div[@class='address']/div/text()")[0]
            print(address)

            # 房屋层数及年代
            flood = on_house.xpath("./div[@class='info clear']/div[@class='flood']/div/text()")[0]
            print(flood)

            # 跟进信息
            followInfo = on_house.xpath("./div[@class='info clear']/div[@class='followInfo']/text()")[0]
            print(followInfo)

            # 页码总数
            page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
            num = json.loads(page_number[0])["totalPage"]
            print(num)
            return None

    def _parse_sold(self,response):
        seletor = etree.HTML(response.body)

        base_xpath = './div[@class="info"]'

        had_saled_houses = seletor.xpath("//ul[@class='listContent']/li")
        for had_saled_house in had_saled_houses:
            had_sold_title = had_saled_house.xpath(base_xpath + '/div[@class="title"]/a')[0].text
            print(had_sold_title)

            had_sold_address = \
            had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="houseInfo"]/text()')[0]
            print(had_sold_address)

            had_sold_dealDate = \
            had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="dealDate"]/text()')[0]
            print(had_sold_dealDate)

            had_sold_totalPrice = \
            had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="totalPrice"]/span')[0].text
            print(had_sold_totalPrice)

            had_sold_unitPrice = \
            had_saled_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="unitPrice"]/span')[0].text
            print(had_sold_unitPrice)

            had_sold_positionInfo = \
            had_saled_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="positionInfo"]/text()')[0]
            print(had_sold_positionInfo)

            had_sold_saleonborad = \
            had_saled_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]')[
                0].text
            print(had_sold_saleonborad)

            had_sold_dealcycle = \
            had_saled_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]')[
                0].text
            print(had_sold_dealcycle)

        return None

    def _xpath_filter(self,xpath):
        if xpath:
            return xpath[0]
        else:
            return None


