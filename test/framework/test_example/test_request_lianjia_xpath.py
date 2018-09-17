import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urlparse, urlsplit, urlunparse, urljoin
from collections import defaultdict

from test.framework.https.parse_url import _parsed_url_agrs, _parsed

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "https://sh.lianjia.com/ershoufang"
_parsed = urlparse(url)
base_url = urlunparse([_parsed.scheme,_parsed.netloc,"","","",""])
r = requests.get(url,headers=header)
r.encoding = "utf-8"


bs = BeautifulSoup(r.text,'html.parser')
seletor = etree.HTML(r.content)

#/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div
total_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a")
part_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a")

total_urls = {}
for a in total_zone:
    path = a.get('href')
    if path not in ["/ershoufang/chongming/","/ershoufang/shanghaizhoubian/"]:
        name = path.split("/")[-2]
        #print(name)
        new_url =urljoin(base_url,path)
        #print(new_url)
        total_urls[name] = new_url

part_urls = defaultdict(list)
for name,url in total_urls.items():
    r = requests.get(url, headers=header)
    seletor = etree.HTML(r.content)
    part_zone = seletor.xpath("/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a")
    parts = []
    for a in part_zone:
        path = a.get('href')
        new_url =urljoin(base_url,path)
        #print(new_url)
        parts.append((new_url))
    part_urls[name].append(parts)

for name,url in part_urls.items():
    print(name,url)