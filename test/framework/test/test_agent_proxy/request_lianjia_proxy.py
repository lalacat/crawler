import pprint
import re

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

r = session.get("https://sh.lianjia.com/xiaoqu/anshan",headers=header,proxies=proxies)
r.encoding = "utf-8"
seletor = etree.HTML(r.content)

#  总小区数
total_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]

# 所有小区列表
all_communities = seletor.xpath('/html/body/div[4]/div[1]/ul/li')
for community in all_communities:
    result = dict()
    # 小区总信息
    community_info = community.xpath('./div[@class="info"]')[0]

    # 小区名称
    community_name = community_info.xpath('./div[@class="title"]/a')[0].text
    result["community_name"] = community_name
    print(community_name)

    # 小区url
    community_url = community_info.xpath('./div[@class="title"]/a')[0].get('href')
    result["community_url"] = community_url
    print(community_url)

    # 小区房屋信息
    community_sale_num = community_info.xpath('./div[@class="houseInfo"]/a[1]')[0].text
    community_rent_num = community_info.xpath('./div[@class="houseInfo"]/a[2]')[0].text
    community_onsale_num = community_info.xpath('../div[@class="xiaoquListItemRight"]/div[2]/a/span/text()')[0]

    result["community_sale_num"] = re.findall('\d+',community_sale_num)[1]
    result["community_rent_num"] = re.findall('\d+',community_rent_num)[0]
    result["community_onsale_num"] = community_onsale_num

    print(community_sale_num,re.findall('\d+',community_sale_num)[1])
    print(community_rent_num,re.findall('\d+',community_rent_num)[0])
    print("正在出售的房屋有：%s"%community_onsale_num)
    # 小区年限
    community_bulid_year = community_info.xpath('./div[@class="positionInfo"]/text()')[3].replace('/',"").strip()
    if str(community_bulid_year) == '未知年建成':
        print(community_bulid_year)
    else:
        print(community_bulid_year,re.findall('\d+',community_bulid_year)[0])
    result["community_bulid_year"] = community_bulid_year


    # 小区均价/html/body/div[4]/div[1]/ul/li[1]/div[2]
    community_avr_price = community_info.xpath('../div[@class="xiaoquListItemRight"]/div/div/span/text()')[0]
    result["community_avr_price"] = community_avr_price

    print(community_avr_price)
    print("\n")


