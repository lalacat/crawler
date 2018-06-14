from test.spider import BaseSpider,Request


class Spider2():
    name = "task2"
    url = 'https://www.smzdm.com/homepage/json_more?p='

    def __init__(self):
        #self.q = queue.Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(10,20):
            i = str(i)
            u = self.url + i
            start_url.append(u)

        self. num = start_url.__len__()

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print('parse1', url)
        i = 1
        for i in range(1):
            # time.sleep(1)
            i += 1
            # print(i)
        return i