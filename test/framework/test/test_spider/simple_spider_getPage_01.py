class SimpleSpider(object):
    """
    将所有小区的地址都写入数据库中
    """
    def __init__(self):
        self.name = ""
        self._start_urls = []
        self.handler_db = True
        self.total_number_community = 0
        self.all_zones = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, info):
        base_name = "SpiderTask: "
        self._name = base_name+info

    @property
    def start_urls(self):
        return self._start_urls

    @start_urls.setter
    def start_urls(self,urls):
        if not isinstance(urls,list):
            self._start_urls = [urls]
        else:
            self._start_urls = urls

    def start_requests(self):
        for i in self.start_urls:
            self.start_urls.remove(i)
            print(i)


