from test.spider import BaseQylSpider,Request
from bs4 import BeautifulSoup

class QylSpider(BaseQylSpider):
    name = "QYL-1"
    url =  "http://www.qyl63.com/recent/"
    db_name = "QYL"
    def __init__(self):
        #self.q = queue.Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(20):
            if i < 1:
                u = self.url
            elif i > 1 :
                i = str(i)
                u = self.url + i
            start_url.append(u)

        self. num = start_url.__len__()

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print("解析网页：", url)
        try:
            bs_obj = BeautifulSoup(context, "html.parser")
            ul = bs_obj.find("ul", "videos")
            lis = ul.find_all("li")
            results = list()
            for l in lis:
                result = dict()
                href_temp = l.a.get("href")
                result["href"] = "http://www.qyl63.com" + href_temp
                result["title"] = l.a.get("titile")
                result["img"] = l.a.div.img.get("src")
                results.append(result)
        except Exception as e:
            print(e)
        return results

