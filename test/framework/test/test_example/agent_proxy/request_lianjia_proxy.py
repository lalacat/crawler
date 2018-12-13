import pprint

import requests
from bs4 import BeautifulSoup
from lxml import etree
from requests.auth import HTTPProxyAuth

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
proxies = {
    "http": "http://spider:123456@47.105.165.81:5527/",
    'https':"http://spider:123456@47.105.165.81:5527/",
}
auth = HTTPProxyAuth('spider','123456')
session=requests.Session()

r = session.get("https://baidu.com",headers=header,proxies=proxies)
r.encoding = "utf-8"
for key,name in r.headers.items():
    print(key+':'+name)
print(r.status_code)
# bs = BeautifulSoup(r.text,'html.parser')
# total_house = bs.find_all("h2",class_='total fl')[0].span.string
# house_list = bs.find_all("ul",class_='sellListContent')[0]
# print(total_house)
# print(len(house_list))
# for i in house_list:
#     print(i.find("div",class_="title").a.string)



