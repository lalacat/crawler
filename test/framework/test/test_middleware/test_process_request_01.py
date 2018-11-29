import random

from twisted.web.http_headers import Headers


class Change_Request_Header(object):

    def __init__(self,crawler):
        self._settings = crawler.settings
        self._headers = self._settings["HEADER_COLLECTION"]
        self.used_header = set()


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        if request.meta.get('header_flag'):
            if request.meta['header_flag']:
                if request.meta.get('last_header'):
                    last_header = request.meta['last_header']
                    new_header = Headers({'User-Agent':random.choice(self._headers)})
                    while new_header == last_header:
                        new_header = Headers({'User-Agent':random.choice(self._headers)})
                        # self.used_header.add(new_header)
        else:
            new_header = Headers({'User-Agent':random.choice(self._headers)})
            # self.used_header.add(new_header)
        request.headers = new_header
        return None
