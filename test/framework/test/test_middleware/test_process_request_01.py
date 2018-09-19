import random


class Change_Request_Header(object):

    def __init__(self,crawler):
        self._settings = crawler.settings
        self._headers = self._settings["HEADER_COLLECTION"]

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        request.headers.setRawHeaders("User-Agent", random.choice(self._headers))

