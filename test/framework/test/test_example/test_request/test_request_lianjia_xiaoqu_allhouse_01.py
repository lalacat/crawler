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

start_time = time.clock()

r = requests.get(on_sale_url,headers=header)
r.encoding = "utf-8"

seletor = etree.HTML(r.content)
houses = seletor.xpath("//ul[@class='sellListContent']")
houses_list = houses[0].xpath('./li')
print(len(houses_list))

total_num = seletor.xpath('//div/h2[@class="total f1"]/span/text()')
