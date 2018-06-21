from bs4 import BeautifulSoup

class BaseSpider(object):
    pass
class Request(object):
    def __init__(self, url, parse):
        self.url = url
        self.parse = parse


class BaseQylSpider(object):


    def get_qyl163_content(self,content):
        print("parse")
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
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