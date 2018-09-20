import requests
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "https://sh.lianjia.com/ershoufang"

beicai = "https://sh.lianjia.com/ershoufang/beicai"


#r = requests.get(url,headers=header,)
''' 
seletor = etree.HTML(r.content)
#  houseItems = seletor.xpath("//div[@class='title']")
listItems = seletor.xpath("/html/body/div[4]/div[1]/ul/li")
#  print(len(houseItems))
print(len(listItems))
i = 0
for item in listItems:
   a = item.find('./a')
   div = item.find("./div/div/a")
   if isinstance(div,_Element):
        #print(a.get("href"))
        i +=1
        #print(div.text)
'''
one_item ="https://sh.lianjia.com/ershoufang/107100505678.html"

r = requests.get(one_item,headers=header)
seletor = etree.HTML(r.content)
total_price = seletor.xpath("/html/body/div[5]/div[2]/div[2]/span[1]")
unitPrice = seletor.xpath("/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span")
area = seletor.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[1]')
print(total_price[0].text)
print(unitPrice[0].text)
b = filter(lambda x:str.isdigit(x),area[0].text)
get_area =lambda b: "".join(x for x in b)
print(get_area)

communityName = seletor.xpath("/html/body/div[5]/div[2]/div[4]/div[1]/a[1]")
print(communityName[0].text)

