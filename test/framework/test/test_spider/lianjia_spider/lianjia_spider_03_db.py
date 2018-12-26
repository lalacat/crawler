from collections import defaultdict
from urllib.parse import urljoin, urlparse, urlunparse
from lxml import etree
from test.framework.spider import Spider
from test.framework.https.request import Request


class LJSpider(Spider):

     name = "LianJia_01"
     custom_settings = ["URL = https://sh.lianjia.com/ershoufang/"]
     def __init__(self):
        super(LJSpider,self).__init__()
        self._url = self.settings["URL"]
        _parsed = urlparse(self._url)
        self.base_url = urlunparse([_parsed.scheme, _parsed.netloc, "", "", "", ""])
        self.collection = "Total Zone"
        self._total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)','Gecko/20100101','Firefox/31.0'],'content-type':['application/json']}
        self._item_num = 0
        self._maxnum = 1
        self.download_delay = 0
        self.flag = False
        self.part_urls = defaultdict(list)

        self.handler_db = True

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
            yield Request(url,callback=self._parse,headers=self.headers,
                          #meta={"download_redirect":True}
                          )
     def _parse(self,response):
        #web_body = BeautifulSoup(response.body,"html.parser")
        seletor = etree.HTML(response.body)
        total_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a")
        total_urls = {}
        for a in total_zone:
            path = a.get('href')
            if path not in ["/ershoufang/chongming/", "/ershoufang/shanghaizhoubian/","/ershoufang/jinshan/"]:
                name = path.split("/")[-2]
                #print(name)
                new_url = urljoin(self.base_url, path)
                #print(new_url)
                total_urls[name] = new_url
        for name,url in total_urls.items():
            yield Request(url,callback=self._parse2,headers=self.headers,meta={'part_name':name})
     def _parse2(self,response):
        name = response.requset.meta["part_name"]
        seletor = etree.HTML(response.body)
        part_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a")
        parts = []
        for a in part_zone:
            path = a.get('href')
            new_url = urljoin(self.base_url, path)
            # print(new_url)
            parts.append((new_url))
        self.part_urls[name].append(parts)

        yield {"part_zone_name":name,"part_zone_url":parts}