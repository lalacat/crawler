import requests
import time
from lxml import etree
from lxml.html import soupparser
"""
测试动态页面的信息提取
Request URL: https://www.smzdm.com/homepage/json_more?timesort=152630225039&p=2
由固定地址+时间戳+页码构成
提取的数据包括：
article_id：文章编码 （可以去重）
article_title：文章标题
article_price：价格
article_mall：购买商场
article_pic：商品图片
article_link：购买界面
article_url：什么值得买商品界面
article_channel_class：文章标签（好价，好文，原创等等）
top_category:商品类别
"""
headers = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = 'https://www.smzdm.com/homepage/json_more?p='


#读网页
def get_url(url):
    webpage = requests.get(url,headers=headers)
    webpage.encoding = 'utf-8'
    # 返回的数据是json格式的，数据类型是dicts
    #其中键data对应的是该页面所有的商品数据，值是list类型
    datas = webpage.json()
    return datas


def get_need_datas(datas):
    datas_list = list()
    datas = datas['data']
    print(type(datas))
    for d in datas:

        result = dict()
        #Python 3.X 里不包含 has_key() 函数，被 __contains__(key) 替代:
        #标签是：z-tag-zixun 没有article_price，article_link，top_category

        if d.__contains__("article_id"):
            result["article_id"] = d["article_id"]
            if d.__contains__("article_title"):
                result["article_title"] = d["article_title"]

            if d.__contains__("article_price"):
                result["article_price"] = d["article_price"]

            if d.__contains__("article_mall"):
                result["article_mall"] = d["article_mall"]

            if d.__contains__("article_pic"):
                result["article_pic"] = d["article_pic"]

            if d.__contains__("article_link"):
                result["article_link"] = d["article_link"]

            if d.__contains__("article_url"):
                result["article_url"] = d["article_url"]

            if d.__contains__("article_channel_class"):
                result["article_channel_class"] = d["article_channel_class"]

            if d.__contains__("top_category"):
                result["top_category"] = d["top_category"]
            datas_list.append(result)
    return datas_list


def print_result(datas_list,url):
    print("页面 :%s 有 %d 件商品"%(url,len(datas_list)))
    for d_l in datas_list:
        for p,d in d_l.items():
            print(p,d)
    print("==============================")


if __name__ == "__main__":
    total = list()
    for i in range(10):
        i = str(i)
        u = url+i
        print(u)

        g_w = get_url(u)
        gnd = get_need_datas(g_w)
        print_result(gnd,u)





'''
datas = result['data']

print(type(datas))
print(len(datas))
print(type(datas[0]))
print(len(datas[0]))

for k,v in datas[0].items():
    print("%s:%s"%(k,v))


value = datas[0]["article_content_all"]
print(value)
'''

