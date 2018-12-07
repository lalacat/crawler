import time

from twisted.internet import defer, reactor

from spider import Spider
from test.framework.core.crawler import Crawler
from test.framework.https.request import Request

from test.framework.setting import Setting


class LJSpider(Spider):

    name = "LianJia_01"
    # custom_settings = ["URL = https://sh.lianjia.com/ershoufang/"]

    def __init__(self):
        super(LJSpider,self).__init__()
        self._url = 'https://sh.lianjia.com/ershoufang/'
        self._total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)','Gecko/20100101','Firefox/31.0'],'content-type':['application/json']}
        self._item_num = 0
        self._maxnum = 3
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
        # web_body = BeautifulSoup(response.body,"html.parser")
        print(response.url+" :"+str(response.request.meta['download_latency']))


        return None


print(time.clock())
settings = Setting()
crawler_01 = Crawler(LJSpider,settings)
c1 = crawler_01.crawl()
c1.addBoth(lambda _:print(time.clock()))
c1.addBoth(lambda _:reactor.stop())
reactor.run()