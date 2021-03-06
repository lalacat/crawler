from spider import Spider,Request,BaseSpider
from test.public_api.web import get_smzdm_datas,print_smzdm_result


class Spider1(Spider):
    name = "task1"
    custom_settings = ["URL = https://www.smzdm.com/homepage/json_more?p="]

    def __init__(self):
        #self.q = queue.Queue()
        #Spider.__init__(self)
        super(Spider1,self).__init__()
        self.url = self.settings["URL"]
        #self.url = "URL = https://www.smzdm.com/homepage/json_more?p=1"

    def start_requests(self):
        start_url = list()

        for i in range(1):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print("解析网页：", url)
        try:
            list = get_smzdm_datas(context)
            print_smzdm_result(list,url)
            #list.append({"url":url})
        except Exception as e:
            self.logger(e)
        return list

