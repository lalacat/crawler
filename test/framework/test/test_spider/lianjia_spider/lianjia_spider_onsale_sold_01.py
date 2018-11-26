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
            if 'chengjiao' in url:
                yield Request(url,callback=self._parse_sold)
            elif 'ershoufang' in url:
                yield Request(url,callback=self._parse_sale)
            else:
                print(url+'出错！！')


    def _parse_sale(self,response):
        seletor = etree.HTML(response.body)
        print(self.name)
        # 所有的在售房屋列表
        try:
            total_house = self._xpath_filter(seletor.xpath("//ul[@class='sellListContent']"))
            if total_house is None:
                total_house = self._xpath_filter(seletor.xpath("//ul[@class='sellListContent LOGCLICKDATA']"))
            if total_house is None:
                print(" ")
                return None
            houses = total_house.xpath('./li')
            print((len(houses)))
            # 总的套数

            # total_num = seletor.xpath('//h2[@class="total f1"]/span/text()')
            total_num = seletor.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()')
            print(response.url+': '+str(total_num))

            # for on_house in houses:
            #     # 总价及均价
            #     total_price = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice']/span/text()"))
            #     print(str(total_price)+'万')
            #
            #     unit_prince = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()"))
            #     print('均价: '+unit_prince)
            #
            #     # 小区名称及网址
            #     title = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='title']/a/text()"))
            #     title_url = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='title']/a/@href"))
            #     print('小区名称: '+title)
            #     print('小区url: '+title_url)
            #
            #     # 小区地址
            #     address = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='address']/div/text()"))
            #     print('小区地址: '+address)
            #
            #     # 房屋层数及年代
            #     flood = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='flood']/div/text()"))
            #     print('房屋层数及年代: '+flood)
            #
            #     # 跟进信息
            #     followInfo = self._xpath_filter(on_house.xpath("./div[@class='info clear']/div[@class='followInfo']/text()"))
            #     print('跟进信息: '+followInfo)
            #
            #     # 页码总数
            #     # page_number = self._xpath_filter(seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data"))
            #     # if page_number:
            #     #     num = json.loads(page_number)["totalPage"]
            #     #     print(num)

        except Exception as e:
            raise Exception(e)
        return None

    def _parse_sold(self,response):
        seletor = etree.HTML(response.body)
        # print(url)
        try:
            base_xpath = './div[@class="info"]'

            had_saled_houses = self._xpath_filter(seletor.xpath("//ul[@class='listContent']")).xpath('./li')
            print(len(had_saled_houses))
            for had_saled_house in had_saled_houses:
                had_sold_title = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="title"]/a/text()'))
                print(had_sold_title)

                had_sold_address = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="houseInfo"]/text()'))
                print(had_sold_address)

                had_sold_dealDate = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="dealDate"]/text()'))
                print(had_sold_dealDate)

                had_sold_totalPrice = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="address"]/div[@class="totalPrice"]/span/text()'))
                print(had_sold_totalPrice)

                had_sold_unitPrice = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="unitPrice"]/span/text()'))
                print(had_sold_unitPrice)

                had_sold_positionInfo = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="positionInfo"]/text()'))
                print(had_sold_positionInfo)

                had_sold_saleonborad = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]/text()'))

                print(had_sold_saleonborad)

                had_sold_dealcycle = \
                self._xpath_filter(had_saled_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]/text()'))
                print(had_sold_dealcycle)

            return None
        except Exception as e:
            print(e)

    def _xpath_filter(self,xpath):
        if xpath:
            return xpath[0]
        else:
            return None


