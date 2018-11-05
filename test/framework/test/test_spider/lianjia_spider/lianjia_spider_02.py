import json
from spider import Spider
from test.framework.https.request import Request
from bs4 import BeautifulSoup

class LJSpider(Spider):

    name = "LianJia_01"
    custom_settings = ["URL = https://sh.lianjia.com/ershoufang/"]

    def __init__(self):
        super(LJSpider,self).__init__()
        self._url = self.settings["URL"]
        self._total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)','Gecko/20100101','Firefox/31.0'],'content-type':['application/json']}
        self._item_num = 0
        self._maxnum = 5
        self.download_delay = 0
        self.flag = False
    def start_requests(self):
        start_url = list()

        for i in range(1,self._maxnum):
            if i == 1 :
                url = self._url
            else:
                i = str(i)
                url = self._url +"pg"+i
            start_url.append(url)

        for url in start_url:
            yield Request(url,callback=self._parse,headers=self.headers,
                          #meta={"download_redirect":True}
                          )

    def _parse(self,response):
        web_body = BeautifulSoup(response.body,"html.parser")

        total_house = web_body.find_all("h2", class_='total fl')[0].span.string
        if total_house:
            self._total_house = total_house

        house_list = web_body.find_all("ul", class_='sellListContent')[0]
        if None in house_list:
            none_num = house_list.count(None)
        else:
            none_num = 0
        one_page_numeber = len(house_list) - none_num
        self._item_num += one_page_numeber
        print(self._item_num)

        urls = []
        for i in range(5,10):
            if i == 1 :
                url = self._url
            else:
                i = str(i)
                url = self._url +"pg"+i
                urls.append(url)
        if not self.flag:
            self.flag = True
            for url in urls:
                yield Request(url,callback=self._parse,headers=self.headers,
                              #meta={"download_redirect":True}
                              )
        else:
            return None