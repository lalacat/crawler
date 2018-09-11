import requests
from bs4 import BeautifulSoup
from lxml import etree


header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
r = requests.get("https://sh.lianjia.com/ershoufang/pg2/",headers=header)
r.encoding = "utf-8"
bs = BeautifulSoup(r.text,'html.parser')
total_house = bs.find_all("h2",class_='total fl')[0].span.string
house_list = bs.find_all("ul",class_='sellListContent')[0]
print(total_house)
print(len(house_list))
for i in house_list:
    print(i.find("div",class_="title").a.string)
