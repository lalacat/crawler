import pprint

from spider import Spider
from test.framework.https.request import Request
from bs4 import BeautifulSoup


class LJSpiderProxy(Spider):
    name = "LianJia_01"
    custom_settings = ["URL = https://sh.lianjia.com/ershoufang/"]

    def __init__(self):
        super(LJSpiderProxy,self).__init__()
        self._url = self.settings["URL"]
        self._total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)'],'content-type':['application/json']}
        self._item_num = 0
        self._maxnum = 1
        self.download_delay = 0
        # self.change_header = True
        # self.proxy = ('47.105.165.81',5527,'spider:123456')
        # self.change_proxy = False

    def start_requests(self):
        start_url = list()
        for i in range(1,self._maxnum+1):
            if i == 1 :
                url = self._url
            else:
                i = str(i)
                url = self._url +"pg"+i
            start_url.append(url)
            for url in start_url:
                yield Request(url,callback=self._parse,headers=self.headers
                      )

    def _parse(self,response):
         # web_body = BeautifulSoup(response.body,"html.parser")
         # total_house = web_body.find_all("h2", class_='total fl')[0].span.string
         # if total_house:
         #    self._total_house = total_house
         # house_list = web_body.find_all("ul", class_='sellListContent')[0]
         # if None in house_list:
         #    none_num = house_list.count(None)
         # else:
         #    none_num = 0
         # one_page_numeber = len(house_list) - none_num
         # self._item_num += one_page_numeber
         request_headers = response.request.headers
         proxy = response.request.meta.get('proxy',None)
         print(request_headers)
         print(proxy)
         # response_headers = response.headers.getAllRawHeaders()
         # print(request_headers)
         # for i in response_headers:
         #     print(i)
         return None
