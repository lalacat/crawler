import json

from lxml import etree

from test.framework.spider import Spider
from test.framework.https.request import Request


class Part_Zone(Spider):
    name = "Part_Zone"

    '''
    测试浦东新区各个分区的总页数
    '''
    def __init__(self,schedule):
        super(Part_Zone,self).__init__()
        self._total_house = 0
        #self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)'],'content-type':['application/json']}

        self.download_delay = 0
        self.start_urls = schedule["part_zone_url"]
        self.collection = schedule["part_zone_name"].upper()
        self.handler_db = False

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback=self._parse)


    def _parse(self,response):
        seletor = etree.HTML(response.body)
        page_number = json.loads(seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0])["totalPage"]
        yield {response.url.split("/")[-2]:page_number}


