import json

from spider import Spider
from test.framework.https.request import Request
from bs4 import BeautifulSoup

class LJSpider(Spider):

    name = "LianJia_01"
    custom_settings = ["URL = https://sh.lianjia.com/ershoufang/pg"]

    def __init__(self):
        super(LJSpider,self).__init__()
        self.url = self.settings["URL"]
        self.total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)','Gecko/20100101','Firefox/31.0'],'content-type':['application/json']}

    def start_requests(self):
        start_url = list()

        for i in range(1,2):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            yield Request(url,callback=self._parse,headers=self.headers,
                          #meta={"download_redirect":True}
                          )

    def _parse(self,response):
        bs4 = BeautifulSoup(response.body,"html.parser")
        self.total_house = bs4.h2
        print(self.total_house)
