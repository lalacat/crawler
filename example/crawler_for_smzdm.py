from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from example.selenium_phantomJS import Smzdm_api
import pymongo
import re
"""
    初始化主页面：
    1. 设置表头
    2. 设置数据库
"""
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = "MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"
url = 'https://www.smzdm.com/'

service_args=[]
service_args.append('--load-images=yes')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true') ##忽略https错误

produce_sorts = ("z-tag-guonei","z-tag-yuanchuang","z-tag-haowu","z-tag-zixun")

"""
设置数据库
"""
smzdm_client = pymongo.MongoClient('localhost',27017)
smzdm_db = smzdm_client['test']
smzdm_collection = smzdm_db["smzdm_products"]

t1 = time.time()
driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
#driver = webdriver.Firefox()

"""
设置筛选对象
"""
filters1= "手机|数码"
filters2 = "GB$"

Page_Number = 10
t2 = time.time()
print("初始化时间：%d秒"%(t2-t1))
response = driver.get(url)




t3 = time.time()
print("加载界面时间：%d秒"%(t3-t2))
print("-----------开始爬虫-------------")

smzdm = Smzdm_api()
current_url = smzdm.get_new_ul(driver)
smzdm_production_list = smzdm.get_new_list(driver)

current_page = smzdm.get_page_numeber_current(current_url)
c_n = int(current_page.text)
print(c_n)
page_web_current = smzdm.get_page_web(current_page)
next_page = smzdm.get_page_numeber_next(current_url)
page_web_next = smzdm.get_page_web(next_page)
temp = {'title':" ",'tag':" ",'price':" ",'picture': ' ','web': " "}

while int(current_page.text) <= Page_Number:
    t_begin = time.time()
    print("当前页： %s => %s " %(current_page.text, page_web_current))

    for s_p_l in smzdm_production_list:
        produce_title = smzdm.has_ElementExist_h5(s_p_l)
        if produce_title != None:
            t_inner_begin = time.time()
            #print("==========")
            m = re.search(filters2,produce_title)
            if m is not None :
                print("title: %s" % produce_title)




            i1 = smzdm_collection.find({'title': produce_title})
            if i1.count() < 1 :


                produce_sort = smzdm.get_new_tag(s_p_l)
                print("tag: %s" %produce_sort)
                temp['tag'] = produce_sort
                if produce_sort == produce_sorts[0]:
                    # 商品价格
                    produce_price = s_p_l.find_element_by_tag_name("span").text
                    print("price: %s" % produce_price)
                    temp['price'] = produce_price

                # 图片地址
                produce_pic = s_p_l.find_element_by_tag_name("img").get_attribute('src')
                print("Picture: %s" % produce_pic)
                temp['picture'] = produce_pic
                # download_pic(produce_price,produce_pic)
                # 商品网站
                produce_web = s_p_l.find_element_by_tag_name("a").get_attribute("href")
                print('网站：%s' % produce_web)
                temp['web'] = produce_web
                smzdm_collection.insert(temp)
                temp.clear()

            t_inner_end = time.time()
            #print("========== %3.1f s" %(t_inner_end - t_inner_begin))
            #print("        ")
    #time.sleep(1)
    driver.get(page_web_next)
    t_next = time.time()
    #print("--- %3.1f s--------"%(t_next-t_inner_end))
    current_url = smzdm.get_new_ul(driver)
    current_page = smzdm.get_page_numeber_current(current_url)
    page_web_curent = smzdm.get_page_web(current_page)
    next_page = smzdm.get_page_numeber_next(current_url)
    page_web_next = smzdm.get_page_web(next_page)
    smzdm_production_list = smzdm.get_new_list(driver)

    t_end = time.time()

    print("========================end with================> %3.1f s" %(t_end - t_begin))
smzdm_client.close()
t_end = time.time()
print("-----------爬虫运行时间：%3.1f s-------------"%(t_end-t3))
