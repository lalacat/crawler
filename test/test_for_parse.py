
class Requset(object):
    def __init__(self,url,callback):
        self.url = url
        self.callback = callback
        print("inner")


class Spider(object):
    name = "smzdm"
    def start_requests(self):
        start_url = ["http://www.baidu.com","http://www.bing.com",]
        for url in start_url:
            print(url)
            yield Requset(url,self.parse)

    def parse(self,response):
        print("---------response--------->",response)
        yield Requset('http://www.cnblogs.com',callback=self.parse)


s = Spider()
a = s.start_requests()
a.__next__()
