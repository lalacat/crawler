from test.spider import BaseSpider,Request
from test.public_api.web import get_need_datas,print_result


class Spider5(BaseSpider):
    name = "task5"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        #self.q = queue.Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(800,1000):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        self. num = start_url.__len__()

        for url in start_url:
            yield Request(url,self._parse)


    def _parse(self,context, url):
        print("解析网页：", url)
        try:
            list = get_need_datas(context)
            #print_result(list,url)
            list.append({"url":url})
        except Exception as e:
            print(e)
        return list