import logging

from test.framework.spider import Spider
from test.framework.https.request import Request


class Test_Spider_3(Spider):
    name = "test3"
    custom_settings = ["URL = https://www.smzdm.com/homepage/json_more?p="]

    def __init__(self):
        super(Test_Spider_3,self).__init__()
        self.url = self.settings["URL"]

    def start_requests(self):
        start_url = list()

        for i in range(20,30):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        for url in start_url:
            yield Request(url,callback=self._parse)


    def _parse(self,content):
        logging.info(content)
        return content



