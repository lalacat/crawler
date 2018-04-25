import requests
from bs4 import BeautifulSoup
from lxml import etree


header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
r = requests.get("https://www.smzdm.com/",headers=header)
r.encoding = "utf-8"
bs = BeautifulSoup(r.text,'lxml')

#smzdm_produce = bs.find('ul', id='feed-main-list')


#smzdm_produce = bs.xpath("body/div[@id='content']")

xml = etree.HTML(r.text)
#print(xml)
smzdm_produce = xml.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                          "/div[@class='feed-main-con']/ul[@id='feed-main-list']")
ul = smzdm_produce[0].xpath('./li')
for u in ul :
    web = u.xpath('./h5/a/@href')
    print(web)

#lists = smzdm_produce.find_all("li","")
#print(type(smzdm_produce))
#print(ul)