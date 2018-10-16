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

print("单个房屋信息：")
#  总价
total_price = seletor.xpath("/html/body/div[5]/div[2]/div[2]/span[1]")
print(total_price[0].text)
#  均价
unitPrice = seletor.xpath("/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span")
print(unitPrice[0].text)
#  房屋面积
area = seletor.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[1]')[0].text
area_str = filter(lambda x:str.isdigit(x) or x=='.',area)
get_area =lambda b: "".join(x for x in b)
print(get_area(area_str))
#  房龄
buildYear = seletor.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[2]')[0].text
buildYear_str = filter(lambda x:str.isdigit(x) or x=='.',buildYear)
get_year =lambda b: "".join(x for x in b)
print(get_year(buildYear_str))
# 小区名称
communityName = seletor.xpath("/html/body/div[5]/div[2]/div[4]/div[1]/a[1]")
print(communityName[0].text)
#  户型
base_inform = seletor.xpath("//*[@id='introduction']/div/div/div[1]/div[2]/ul/li")
for i in [base_inform[0],base_inform[2]]:
    print(i.xpath("./span/text()")[0],i.xpath("./text()")[0])
#  挂牌时间，上次交易时间
transaction = seletor.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li')
for i in [transaction[0],transaction[2]]:
    print(i.xpath("./span/text()")[0],i.xpath("./span[2]/text()")[0])
