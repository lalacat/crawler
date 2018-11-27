import json
import re
import time
from urllib.parse import urlparse, urlunparse, urljoin

import requests
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "https://sh.lianjia.com/xiaoqu/5011000017281/"
had_saled = r'chengjiao'
on_sale = r'ershoufang'
community_name = url.split('/')[-2]
had_saled_url =re.sub(community_name,'c'+community_name, re.sub(r'xiaoqu','chengjiao',url))
on_sale_url =re.sub(community_name,'c'+community_name, re.sub(r'xiaoqu','ershoufang',url))

print(had_saled_url)
print(on_sale_url)
# "/html/body/div[5]/div[1]/div[2]/div[1]/span"
# '/html/body/div[4]/div[1]/div[2]/h2/span/text()'


r = requests.get(on_sale_url,headers=header)
r.encoding = "utf-8"

seletor = etree.HTML(r.content)

# 所有的在售房屋列表
# houses = seletor.xpath("//ul[@class='sellListContent']")[0].xpath('./li')

# print(len(houses))

# 总的套数
total_num_01 = seletor.xpath('//h2[@class="total fl"]/span/text()')[0]
print(total_num_01)


""" 
# 总价及均价
total_price = houses[0].xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice']/span")[0].text
unit_prince = houses[0].xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span")[0].text
print(total_price)
print(unit_prince)

# 小区名称及网址
title = houses[0].xpath("./div[@class='info clear']/div[@class='title']/a")[0].text
title_url = houses[0].xpath("./div[@class='info clear']/div[@class='title']/a/@href")[0]
print(title)
print(title_url)

# 小区地址
address = houses[0].xpath("./div[@class='info clear']/div[@class='address']/div/text()")[0]
print(address)

# 房屋层数及年代
flood = houses[0].xpath("./div[@class='info clear']/div[@class='flood']/div/text()")[0]
print(flood)

# 跟进信息
followInfo = houses[0].xpath("./div[@class='info clear']/div[@class='followInfo']/text()")[0]
print(followInfo)

# 页码总数
page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
num = json.loads(page_number[0])["totalPage"]
print(num)









r = requests.get(had_saled_url,headers=header)
r.encoding = "utf-8"

seletor = etree.HTML(r.content)

base_xpath='./div[@class="info"]'

had_saled_houses = seletor.xpath("//ul[@class='listContent']/li")

total_num_01 = seletor.xpath('//div[@class="total fl"]/span/text()')[0]

had_sold_title = had_saled_houses[0].xpath(base_xpath+'/div[@class="title"]/a')[0].text
print(had_sold_title)

had_sold_address = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="houseInfo"]/text()')[0]
print(had_sold_address)

had_sold_dealDate = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="dealDate"]/text()')[0]
print(had_sold_dealDate)

had_sold_totalPrice = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="totalPrice"]/span')[0].text
print(had_sold_totalPrice)

had_sold_unitPrice = had_saled_houses[0].xpath(base_xpath+'/div[@class="flood"]/div[@class="unitPrice"]/span')[0].text
print(had_sold_unitPrice)

had_sold_positionInfo = had_saled_houses[0].xpath(base_xpath+'/div[@class="flood"]/div[@class="positionInfo"]/text()')[0]
print(had_sold_positionInfo)

had_sold_saleonborad = had_saled_houses[0].xpath(base_xpath+'/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]')[0].text
print(had_sold_saleonborad)

had_sold_dealcycle = had_saled_houses[0].xpath(base_xpath+'/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]')[0].text
print(had_sold_dealcycle)
"""