from urllib.parse import urlparse, urlunparse, urljoin

import requests
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "https://sh.lianjia.com/xiaoqu/pudong/"

_parsed = urlparse(url)
base_url = urlunparse([_parsed.scheme,_parsed.netloc,"","","",""])
r = requests.get(url,headers=header)
r.encoding = "utf-8"

seletor = etree.HTML(r.content)
part_zone = seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a")

total_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
print(total_number_community)
part_numbers= []

for a in part_zone:
    path = a.get('href')
    name = path.split('/')[-2]
    new_url = urljoin(base_url, path)
    r = requests.get(new_url, headers=header)
    seletor = etree.HTML(r.content)
    part_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]
    #print(name)
    #print(new_url)
    # print(part_number_community)
    part_numbers.append(part_number_community)

total = 0
for i in part_numbers:
    total += int(i)
print(total)
'''
for name,url in total_urls.items():
    r = requests.get(url, headers=header)
    seletor = etree.HTML(r.content)
    page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
    num = json.loads(page_number[0])["totalPage"]
    print(name,num)
 
    part_zone = seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div[2]/a")
    parts = [] #
    for a in part_zone:
        path = a.get('href')
        new_url = urljoin(base_url, path)
        # print(new_url)
        parts.append((new_url))
    part_urls[name].append(parts)
    print(name,parts)

'''