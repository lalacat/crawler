from collections import defaultdict

from bs4 import BeautifulSoup
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

        # 所有的在售房屋列表
        try:
            total_house = self._xpath_filter(seletor.xpath("//ul[@class='sellListContent']"))
            if total_house is None:
                total_house = self._xpath_filter(seletor.xpath("//ul[@class='sellListContent LOGCLICKDATA']"))
            if total_house is None:
                print(response.url+':0')
                return None
            houses = total_house.xpath('./li')

            # 总的套数
            total_num = seletor.xpath('//h2[@class="total fl"]/span/text()')
            print('sale：'+response.url+': '+str(total_num)+"==="+str(len(houses)))

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
        bs_obj = BeautifulSoup(response.body, "html.parser")
        if response.url == 'https://sh.lianjia.com/chengjiao/c5012200974233196/':
            print(bs_obj)
        try:
            base_xpath = './div[@class="info"]'

            sold_houses = self._xpath_filter(seletor.xpath("//ul[@class='listContent']")).xpath('./li')
            # total_num = seletor.xpath('//div[@class="total fl"]/span/text()')
            total_num = seletor.xpath("/html/body/div[5]/div[1]/div[2]/div[1]/span/text()")[0]


            print("sold："+response.url+': '+str(total_num)+"==="+str(len(sold_houses)))
            return None

            # for sold_house in sold_houses:
            #     sold_title = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="title"]/a/text()'))
            #     print("小区名称："+sold_title)
            #
            #     sold_address = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="houseInfo"]/text()'))
            #     print("小区地址："+sold_address)
            #
            #     sold_dealDate = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="dealDate"]/text()'))
            #     print("成交日期："+sold_dealDate)
            #
            #     sold_totalPrice = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="totalPrice"]/span/text()'))
            #     print("成交价格："+sold_totalPrice)
            #
            #     sold_unitPrice = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="unitPrice"]/span/text()'))
            #     print('成交均价：'+sold_unitPrice)
            #
            #     sold_positionInfo = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="positionInfo"]/text()'))
            #     print("楼层高度："+sold_positionInfo)
            #
            #     sold_saleonborad = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]/text()'))
            #
            #     print("挂牌价："+sold_saleonborad)
            #
            #     sold_dealcycle = \
            #     self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]/text()'))
            #     print("成交周期："+sold_dealcycle)

        except Exception as e:
            print(e)
            # raise Exception(e)
        return None

    def _xpath_filter(self,xpath):
        if xpath:
            return xpath[0]
        else:
            return None


