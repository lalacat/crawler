import json
import re
import time
from urllib.parse import urlparse, urlunparse, urljoin

import requests
from bs4 import BeautifulSoup
from lxml import etree

# header = { 'User-Agent' :
#         'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
#            'content-type':"application/json"}
header = { 'User-Agent' :
               'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
               'content-type':"application/json"}
url = "https://sh.lianjia.com/xiaoqu/5011000017281/"
had_saled = r'chengjiao'
on_sale = r'ershoufang'
community_name = url.split('/')[-2]
had_saled_url =re.sub(community_name,'c'+community_name, re.sub(r'xiaoqu','chengjiao',url))
on_sale_url =re.sub(community_name,'c'+community_name, re.sub(r'xiaoqu','ershoufang',url))

# print(had_saled_url)
# print(on_sale_url)


{'sale_中通雅苑': 'https://sh.lianjia.com/ershoufang/c5011000002697/',
 'sale_书香公寓': 'https://sh.lianjia.com/ershoufang/c5011000016725/',
 'sale_伊顿公寓': 'https://sh.lianjia.com/ershoufang/c5011000009432/',
 'sale_公交新村': 'https://sh.lianjia.com/ershoufang/c5011000011612/',
 'sale_冶金公寓': 'https://sh.lianjia.com/ershoufang/c5011000000534/',
 'sale_华元豪庭': 'https://sh.lianjia.com/ershoufang/c5011000004466/',
 'sale_双辽支路70弄': 'https://sh.lianjia.com/ershoufang/c5011000004404/',
 'sale_双辽新村': 'https://sh.lianjia.com/ershoufang/c5011000003210/',
 'sale_同济新村': 'https://sh.lianjia.com/ershoufang/c5011000009269/',
 'sale_同济绿园': 'https://sh.lianjia.com/ershoufang/c5011000016368/',
 'sale_同济西苑': 'https://sh.lianjia.com/ershoufang/c5011000004433/',
 'sale_君欣豪庭': 'https://sh.lianjia.com/ershoufang/c5011000014671/',
 'sale_和平花苑': 'https://sh.lianjia.com/ershoufang/c5011000017889/',
 'sale_大连西路40弄': 'https://sh.lianjia.com/ershoufang/c5011000005549/',
 'sale_密云小区': 'https://sh.lianjia.com/ershoufang/c5011000015822/',
 'sale_恒联新天地花园': 'https://sh.lianjia.com/ershoufang/c5011000014456/',
 'sale_恒阳花苑': 'https://sh.lianjia.com/ershoufang/c5011000009836/',
 'sale_海上海新城(公寓)': 'https://sh.lianjia.com/ershoufang/c5011000014882/',
 'sale_耀浦苑': 'https://sh.lianjia.com/ershoufang/c5011000014911/',
 'sale_英达苑': 'https://sh.lianjia.com/ershoufang/c5011000004702/',
 'sale_辽源四村': 'https://sh.lianjia.com/ershoufang/c5011000004437/',
 'sale_鞍山一村': 'https://sh.lianjia.com/ershoufang/c5011000012151/',
 'sale_鞍山七村': 'https://sh.lianjia.com/ershoufang/c5011000015792/',
 'sale_鞍山三村': 'https://sh.lianjia.com/ershoufang/c5011000011135/',
 'sale_鞍山五村': 'https://sh.lianjia.com/ershoufang/c5011000014520/',
 'sale_鞍山八村': 'https://sh.lianjia.com/ershoufang/c5011000012841/',
 'sale_鞍山六村': 'https://sh.lianjia.com/ershoufang/c5011000013450/',
 'sale_鞍山四村第一小区': 'https://sh.lianjia.com/ershoufang/c5011000013940/',
 'sale_鞍山四村第三小区': 'https://sh.lianjia.com/ershoufang/c5012200974233196/',
 'sale_鞍山四村第二小区': 'https://sh.lianjia.com/ershoufang/c5012200059612586/'}

sold_urls={
 'sold_中通雅苑': 'https://sh.lianjia.com/chengjiao/c5011000002697/',
 'sold_书香公寓': 'https://sh.lianjia.com/chengjiao/c5011000016725/',
 'sold_伊顿公寓': 'https://sh.lianjia.com/chengjiao/c5011000009432/',
 'sold_公交新村': 'https://sh.lianjia.com/chengjiao/c5011000011612/',
 'sold_冶金公寓': 'https://sh.lianjia.com/chengjiao/c5011000000534/',
 'sold_华元豪庭': 'https://sh.lianjia.com/chengjiao/c5011000004466/',
 'sold_双辽支路70弄': 'https://sh.lianjia.com/chengjiao/c5011000004404/',
 'sold_双辽新村': 'https://sh.lianjia.com/chengjiao/c5011000003210/',
 'sold_同济新村': 'https://sh.lianjia.com/chengjiao/c5011000009269/',
 'sold_同济绿园': 'https://sh.lianjia.com/chengjiao/c5011000016368/',
 'sold_同济西苑': 'https://sh.lianjia.com/chengjiao/c5011000004433/',
 'sold_君欣豪庭': 'https://sh.lianjia.com/chengjiao/c5011000014671/',
 'sold_和平花苑': 'https://sh.lianjia.com/chengjiao/c5011000017889/',
 'sold_大连西路40弄': 'https://sh.lianjia.com/chengjiao/c5011000005549/',
 'sold_密云小区': 'https://sh.lianjia.com/chengjiao/c5011000015822/',
 'sold_恒联新天地花园': 'https://sh.lianjia.com/chengjiao/c5011000014456/',
 'sold_恒阳花苑': 'https://sh.lianjia.com/chengjiao/c5011000009836/',
 'sold_海上海新城(公寓)': 'https://sh.lianjia.com/chengjiao/c5011000014882/',
 'sold_耀浦苑': 'https://sh.lianjia.com/chengjiao/c5011000014911/',
 'sold_英达苑': 'https://sh.lianjia.com/chengjiao/c5011000004702/',
 'sold_辽源四村': 'https://sh.lianjia.com/chengjiao/c5011000004437/',
 'sold_鞍山一村': 'https://sh.lianjia.com/chengjiao/c5011000012151/',
 'sold_鞍山七村': 'https://sh.lianjia.com/chengjiao/c5011000015792/',
 'sold_鞍山三村': 'https://sh.lianjia.com/chengjiao/c5011000011135/',
 'sold_鞍山五村': 'https://sh.lianjia.com/chengjiao/c5011000014520/',
 'sold_鞍山八村': 'https://sh.lianjia.com/chengjiao/c5011000012841/',
 'sold_鞍山六村': 'https://sh.lianjia.com/chengjiao/c5011000013450/',
 'sold_鞍山四村第一小区': 'https://sh.lianjia.com/chengjiao/c5011000013940/',
 'sold_鞍山四村第三小区': 'https://sh.lianjia.com/chengjiao/c5012200974233196/',
 'sold_鞍山四村第二小区': 'https://sh.lianjia.com/chengjiao/c5012200059612586/'}

for sold_url in sold_urls.values():

    r = requests.get(sold_url,headers=header)
    r.encoding = "utf-8"
    seletor = BeautifulSoup(r.content,"html.parser")
    sold_houses = seletor.find('ul',class_='listContent')
    total_num = seletor.find('div',class_="total fl").span.text
    house = sold_houses.li
    print(sold_url+':'+total_num+'===='+str(len(sold_houses)))





# # 在售的总的套数
# houses = seletor.xpath("//ul[@class='sellListContent']")[0].xpath('./li')
# print(len(houses))
#
# total_num_01 = seletor.xpath('//h2[@class="total fl"]/span/text()')[0]
# print(total_num_01)

# 已售的总的套数
# had_saled_houses = seletor.xpath("//ul[@class='listContent']/li")
# print(len(had_saled_houses))
# total_num_01 = seletor.xpath('//div[@class="total fl"]/span/text()')[0]
# print(total_num_01)


# 总价及均价
# total_price = houses[0].xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice']/span")[0].text
# unit_prince = houses[0].xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span")[0].text
# print(total_price)
# print(unit_prince)

# # 小区名称及网址
# title = houses[0].xpath("./div[@class='info clear']/div[@class='title']/a")[0].text
# title_url = houses[0].xpath("./div[@class='info clear']/div[@class='title']/a/@href")[0]
# print(title)
# print(title_url)
#
# # 小区地址
# address = houses[0].xpath("./div[@class='info clear']/div[@class='address']/div/text()")[0]
# print(address)
#
# # 房屋层数及年代
# flood = houses[0].xpath("./div[@class='info clear']/div[@class='flood']/div/text()")[0]
# print(flood)
#
# # 跟进信息
# followInfo = houses[0].xpath("./div[@class='info clear']/div[@class='followInfo']/text()")[0]
# print(followInfo)
#
# # 页码总数
# page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
# num = json.loads(page_number[0])["totalPage"]
# print(num)








#
# r = requests.get(had_saled_url,headers=header)
# r.encoding = "utf-8"
#
# seletor = etree.HTML(r.content)
#
# base_xpath='./div[@class="info"]'
#
# had_saled_houses = seletor.xpath("//ul[@class='listContent']/li")
#
# total_num_01 = seletor.xpath('//div[@class="total fl"]/span/text()')[0]
#
# had_sold_title = had_saled_houses[0].xpath(base_xpath+'/div[@class="title"]/a')[0].text
# print(had_sold_title)
#
# had_sold_address = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="houseInfo"]/text()')[0]
# print(had_sold_address)
#
# had_sold_dealDate = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="dealDate"]/text()')[0]
# print(had_sold_dealDate)
#
# had_sold_totalPrice = had_saled_houses[0].xpath(base_xpath+'/div[@class="address"]/div[@class="totalPrice"]/span')[0].text
# print(had_sold_totalPrice)
#
# had_sold_unitPrice = had_saled_houses[0].xpath(base_xpath+'/div[@class="flood"]/div[@class="unitPrice"]/span')[0].text
# print(had_sold_unitPrice)
#
# had_sold_positionInfo = had_saled_houses[0].xpath(base_xpath+'/div[@class="flood"]/div[@class="positionInfo"]/text()')[0]
# print(had_sold_positionInfo)
#
# had_sold_saleonborad = had_saled_houses[0].xpath(base_xpath+'/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]')[0].text
# print(had_sold_saleonborad)
#
# had_sold_dealcycle = had_saled_houses[0].xpath(base_xpath+'/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]')[0].text
# print(had_sold_dealcycle)
