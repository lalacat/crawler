import json

from lxml import etree

from spider import  Spider
import logging

from test.framework.https.request import Request

logger = logging.getLogger(__name__)

class SimpleSpider(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    def __init__(self):
        self.name = ""
        self._start_urls = []
        self.handler_db = False
        self.total_number_community = 0
        self.all_zones = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, info):
        base_name = "SpiderTask: "
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
            yield Request(url, callback=self._parse)

    def _parse(self,response):
        seletor = etree.HTML(response.body)
        #  获取下属城镇的小区总数
        page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        num = json.loads(page_number[0])["totalPage"]
        logger.debug("%s的总页数是%d" % (self.name, num))
        return None
