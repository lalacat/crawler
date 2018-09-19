from bs4 import BeautifulSoup

from spider import Spider


class Part_Zone(Spider):
    name = "Part_Zone"
    def __init__(self,schedule):
        super(Part_Zone,self).__init__()
        self._total_house = 0
        self.headers = {'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0)'],'content-type':['application/json']}
        self._item_num = 0
        self._maxnum = 2
        self.download_delay = 0
        self.start_urls = schedule["part_zone_url"]
        self.collection = schedule["part_zone_name"].upper()

    def start_requests(self):
        for url in self.start_urls:
            yield url




    def _parse(self,response):
        bs = BeautifulSoup(response.body,'html.parser')
        total_house = bs.find_all("h2",class_='total fl')[0].span.string
        house_list = bs.find_all("ul",class_='sellListContent')[0]
        print(total_house)
        print(len(house_list))
        for i in house_list:
            print(i.find("div",class_="title").a.string)



