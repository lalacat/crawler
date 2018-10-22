from urllib.parse import urljoin, urlparse, urlunparse

from lxml import etree

from spider import Spider
from test.framework.https.request import Request


class Part_Zone(Spider):
    name = "Community"
    """
    测试浦东新区各个分区小区数的总个数，不写入数据库
    """

    def __init__(self,schedule):
        super(Part_Zone,self).__init__()
        self._total_house = 0

        self.download_delay = 0
        self.start_urls = "https://sh.lianjia.com/xiaoqu/pudong/"
        self._parsed = urlparse(self.start_urls)
        self.base_url = urlunparse([self._parsed.scheme, self._parsed.netloc, "", "", "", ""])
        # self.collection = schedule["part_zone_name"].upper()
        self.handler_db = False
        self.total_number_community = 0
        self.part_numbers = {}

    def start_requests(self):
        #for url in self.start_urls:
        yield Request(self.start_urls,callback=self._parse)


    def _parse(self,response):
        seletor = etree.HTML(response.body)
        # 分区的总小区数
        total_number = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
        self.total_number_community = total_number
        #  获取分区下属城镇的地址
        part_zone = seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a")
        for a in part_zone:
            path = a.get('href')
            name = path.split('/')[-2]
            new_url = urljoin(self.base_url, path)
            yield Request(new_url,callback=self._parse2,meta={"zone_name":name})

    def _parse2(self,response):
        seletor = etree.HTML(response.body)
        #  获取下属城镇的小区总数
        part_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
        self.part_numbers[response.requset.meta["zone_name"]] = part_number_community
        return None

