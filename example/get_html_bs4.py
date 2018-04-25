from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
req = request.Request(url='https://www.smzdm.com/', headers=headers)


def download_pic(picture_name, picture_url):
    pu = picture_name.replace(r'/', '')
    with open('..\\pic\\' + pu + '.jpg', 'wb') as f:
        req = request.urlopen(picture_url)
        buf = req.read()
        f.write(buf)


# 好价，好文，好物，视频
sorts = ("z-tag-guonei", "z-tag-yuanchuang", "z-tag-haowu", "z-tag-zixun")

html = request.urlopen(req)

bs_obj = BeautifulSoup(html.read(), "html.parser")
smzdm_produce_lists = bs_obj.find_all('li', 'feed-row-wide')

for produce in smzdm_produce_lists:
    # 标题内容
    smzdm_title = produce.h5.get_text()
    print("title: %s" % smzdm_title)

    # 商品类别
    for sort in sorts:
        smzdm_sort = produce.find('a', sort)
        if smzdm_sort != None:
            print("sort: %s" % smzdm_sort.get_text())
            if sort == sorts[0]:
                # 商品价格
                smzdm_price = produce.span.get_text()
                print("price: %s" % smzdm_price)
                # 图片地址
                smzdm_pic = produce.img.get('src')
                print("Picture: %s" % smzdm_pic)
                # download_pic(smzdm_price,smzdm_pic)

    # 标题链接
    smzdm_address = produce.a.get('href')
    print("网站：%s" % smzdm_address)

    print('-------------------------------------')

html.close()
