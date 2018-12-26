from urllib.parse import urljoin, urlparse, urlunparse

from lxml import etree

from test.framework.spider import Spider
from test.framework.https.request import Request


class Part_Zone(Spider):
    name = "Community"
    """
    将所有小区的地址都写入数据库中
    """

    def __init__(self,schedule):
        super(Part_Zone,self).__init__()
        self._total_house = 0

        self.download_delay = 0
        self.start_url =  "https://sh.lianjia.com/xiaoqu/"
        self._parsed = urlparse(self.start_url)
        self.base_url = urlunparse([self._parsed.scheme, self._parsed.netloc, "", "", "", ""])
        self.collection = "XiaoQu"
        self.handler_db = True
        self.total_number_community = 0
        self.all_zones = {}
        #self.all_towns = []


    def start_requests(self):
        yield Request(self.start_url,callback=self._parse)

    def _parse(self,response):
        seletor = etree.HTML(response.body)
        #  获取所有分区的名称和url
        all_zone = seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div/a")

        for one_zone in all_zone:
            #  获取一个分区的url
            path = one_zone.get('href')
            #  过滤不需要爬的小区
            if path not in ["/xiaoqu/chongming/", "/xiaoqu/shanghaizhoubian/"]:
                name = path.split('/')[-2]
                new_url = urljoin(self.base_url, path)
                self.all_zones[name] = new_url
                yield Request(new_url,callback=self._parse2,meta={"total_zone_name":name})

    def _parse2(self,response):
        seletor = etree.HTML(response.body)
        #  获得各个分区下的城镇
        all_town= seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a")
        all_towns = {}
        for a in all_town:
            path = a.get('href')
            name = path.split('/')[-2]
            new_url = urljoin(self.base_url, path)
            all_towns[name]= new_url

        all_towns["total_zone_name"] = [response.requset.meta["total_zone_name"],response.url]
        yield all_towns