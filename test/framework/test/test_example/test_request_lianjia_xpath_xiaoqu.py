import json
from collections import defaultdict
from urllib.parse import urlparse, urlunparse, urljoin

import requests
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "https://sh.lianjia.com/xiaoqu/"

_parsed = urlparse(url)
base_url = urlunparse([_parsed.scheme,_parsed.netloc,"","","",""])
r = requests.get(url,headers=header)
r.encoding = "utf-8"


seletor = etree.HTML(r.content)
#/html/body/div[3]/div[1]/dl[2]/dd/div/div[1]
total_zone = seletor.xpath("/html/body/div[3]/div[1]/dl[2]/dd/div/div/a")
part_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a")
total_urls = {}
for a in total_zone:
    path = a.get('href')
    if path not in ["/xiaoqu/chongming/","/xiaoqu/shanghaizhoubian/"]:
        name = path.split("/")[-2]
        #print(name)
        new_url =urljoin(base_url,path)
        #print(new_url)
        total_urls[name] = new_url

part_urls = defaultdict(list)
total_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")
print(total_number_community)
for name,url in total_urls.items():
    r = requests.get(url, headers=header)
    seletor = etree.HTML(r.content)
    page_number = seletor.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
    num = json.loads(page_number[0])["totalPage"]
    print(name,num)
    '''
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