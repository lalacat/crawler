from urllib import request
from bs4 import BeautifulSoup

'''
headers = { 'User-Agent'  :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0' }
req  = request.Request(url='https://www.smzdm.com/',headers=headers)


html = request.urlopen(req)

bs_obj = BeautifulSoup(html.read(),"html.parser")
'''
def get_tag(self,smzdm_produce_lists):
    #smzdm_produce_lists = bs_obj.findall('li','feed-row-wide')

    for produce in smzdm_produce_lists:

        #标题内容
        smzdm_title = produce.h5.get_text()
        print("title: %s" %smzdm_title)

        #商品类别
        smzdm_sort = produce.find('a','z-tag-guonei').get_text()
        print("sort: %s" %smzdm_sort)
        #商品价格
        smzdm_price = produce.span.get_text()
        print("price: %s" %smzdm_price)

        #标题链接
        smzdm_address = produce.a.get('href')
        print("网站：%s" %smzdm_address)


        #图片地址
        smzdm_pic = produce.img.get('src')
        print("Picture: %s" %smzdm_pic)
