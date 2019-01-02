import logging

from test.framework.spider import Spider,Request
from test.framework.https.request import Request
from test.public_api.web import get_smzdm_datas


class Test_Spider_1(Spider):
    name = "test1"
    custom_settings = ["URL = https://www.smzdm.com/homepage/json_more?p="]

    def __init__(self):
        super(Test_Spider_1,self).__init__()
        self.url = self.settings["URL"]

    def start_requests(self):
        start_url = list()

        for i in range(100):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            yield Request(url,callback=self._parse)


    def process_request(self,request,spider):
        logging.info("%s process request!!" %self.name)
        return request

    def open_spider(self,content):
        logging.info("%s open spider!!" %self.name)
        return content

    def _parse(self,response):
        logging.info("通过_parse的处理response")
        result = get_smzdm_datas(response.body)
        return result



