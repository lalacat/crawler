from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib import request
import time

class Smzdm_api(object):

    def download_pic(self,picture_name,picture_url):
        pu = picture_name.replace(r'/' ,'')
        with open('.\\pic\\'+pu+'.jpg','wb') as f:
            req = request.urlopen(picture_url)
            buf = req.read()
            f.write(buf)

    def get_new_list(self,driver):
        try:
            return driver.find_element_by_id("feed-main-list").find_elements_by_tag_name("li")
        except NoSuchElementException:
            print("get_new_list error!!")
            return False

    def has_ElementExist_h5(self,list):
        try:
            return list.find_element_by_tag_name("h5").text
        except NoSuchElementException as e:
            #print("has_ElementExist_h5 error!!")
            return None

    def get_new_tag(self,list):
        try:
            return list.find_element_by_xpath(".//div/div/a").get_attribute("class")
        except NoSuchElementException :
            return None


    def get_new_ul(self,driver):
        try:
            return  driver.find_element_by_id("J_feed_pagenation")
        except NoSuchElementException:
            print("get_new_ul error!!")
            return False

    def get_page_numeber_current(self,ul):
        try:
            return ul.find_element_by_xpath("//li[@class='page-number current']")
        except NoSuchElementException :
            print("page_numeber_current!!")
            return False


    def get_page_web(self,page):
        try:
            return page.find_element_by_tag_name("a").get_attribute("href")
        except  NoSuchElementException:
            print("get_page_web error")
            return False

    def get_page_numeber_next(self,ul):
        try:
            return  ul.find_element_by_xpath("//li[@class='page-turn next-page']")
        except NoSuchElementException :
            print("page_numeber_next error!!")
            return False

    #返回值是标签a
    def get_page_select(self,driver,page_number):
        flag = True
        while flag :
            try:
                ul = self.get_new_ul(driver)
                result =  ul.find_element_by_xpath("//li/a[contains(text(),'%s')]" % page_number)
                flag = False
            except NoSuchElementException :
                p_l = self.get_page_number_list(ul)
                if p_l :
                    p_n_l = p_l[len(p_l)-1]
                    if int(page_number)> int(p_n_l.text):
                        p_w = self.get_page_web(p_n_l)
                        driver.get(p_w)
        return result

    def get_page_number_list(self,ul):
        try:
            return ul.find_elements_by_xpath("//li[@class='page-number']")
        except NoSuchElementException:
            return False
        """
        pn_dict = {}
        page_number = ul.find_elements_by_xpath("//li[@class='page-number']")
        for p in page_number:
            page_web = p.find_element_by_tag_name("a").get_attribute("href")
            print(p.text + ":" + page_web + " : " + p.text)
            pn_dict[p.text] = page_web
        """

    def page_scroll(self,driver,n=1,m=1):
        s = "window.scrollTo(0,document.body.scrollHeight/{0}*{1});".format(n, m)
        driver.execute_script(s)
'''
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = "MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"
url = 'https://www.smzdm.com/'
produce_sorts = ("z-tag-guonei","z-tag-yuanchuang","z-tag-haowu","z-tag-zixun")
t1 = time.time()
driver = webdriver.PhantomJS(desired_capabilities=dcap)
#driver = webdriver.Firefox()
driver.maximize_window()
t2 = time.time()
print("初始化时间：%d秒"%(t2-t1))
try:
    driver.get(url)
    wait = WebDriverWait(driver,10)
    wait.until(lambda temp_driver:
               temp_driver.find_element_by_id("J_feed_pagenation").is_displayed())
except NoSuchElementException:
    print("error")

t3 = time.time()
print("加载界面时间：%d秒"%(t3-t2))
test  = Smzdm_api()
p_s = test.get_page_select(driver,20)
p_s_w = p_s.get_attribute("href")
print(p_s_w)
print(p_s.text)
#print("%s:%s"%(type(p_s),p_s))

t4 = time.time()
print("搜索时间：%d秒"%(t4-t3))





#page_number = driver.find_elements_by_xpath("//div/ul/li[@class='page-number']")
page_number_lists = driver.find_element_by_id("J_feed_pagenation")
#p2 = page_number_lists.find_element_by_xpath("//li[@class='page-number'and contains(text(),'3')]")
#p2 = page_number_lists.find_element_by_xpath("//li/a[contains(text(),'3')]")
#p_c = page_numeber_current(page_number_lists)
#p_n = page_numeber_next(page_number_lists)



t1 = time.time()
while int(p_c.text) <= 6:

    t2 = time.time()
    print("page_curren : %s " % p_c.text)
    print("page_next: %s " % p_n.text)

    produce_lists = driver.find_element_by_id("feed-main-list").find_elements_by_tag_name("li")

    for p in produce_lists:
        produce_title = Smzdm_api.has_ElementExist_h5(p)
        if produce_title != None:
            print("title: %s" % produce_title)


    url_next = Smzdm_api.get_next_page(p_n)
    print(url_next)
    driver.get(url_next)

    print("-----------------------------------------------------")
    page_number_lists = driver.find_element_by_id("J_feed_pagenation")
    p_c = Smzdm_api.page_numeber_current(page_number_lists)
    p_n = Smzdm_api.page_numeber_next(page_number_lists)
    t3 = time.time()


    print("加载界面时间：%d秒"%(t3-t2))

t4 =time.time()
print("运行时间： %d" % (t4-t1))
'''
"""
pn_dict = {}
for p in page_number:
    page_web = p.find_element_by_tag_name("a").get_attribute("href")
    print(p.text+":"+page_web + " : " + p.text)
    pn_dict[p.text] =  page_web
url = pn_dict["6"]

t4 = time.time()
driver.get(url)
t5 = time.time()
print("加载界面时间：%d秒"%(t5-t4))

"""

"""
print("第一次滚动")
s = "window.scrollTo(0,document.body.scrollHeight/{0}*{1});".format(1, 1)
#driver.save_screenshot('.\\pic\\1.png')
page_number = driver.find_element_by_xpath("//div/ul/li[@class='page-number current']")

p_lists = page_number.find_elements_by_tag_name("li")
print(p_lists)
for p in p_lists:
    print(p.text)

time.sleep(3)
print(time.time()-t3)
print("第二次滚动")

driver.execute_script(s)
#driver.save_screenshot('.\\pic\\2.png')
time.sleep(3)

page_number = driver.find_element_by_xpath("//div/ul/li[@class='page-number current']")
page_web = page_number.find_element_by_tag_name("a").get_attribute("href")
print(page_web +" : " + page_number.text)
print("第三次滚动")

driver.execute_script(s)
page_number = driver.find_element_by_xpath("//div/ul/li[@class='page-number current']")
page_web = page_number.find_element_by_tag_name("a").get_attribute("href")
print(page_web +" : " + page_number.text)
#driver.save_screenshot('.\\pic\\3.png')


produce_lists = driver.find_element_by_id("feed-main-list").find_elements_by_tag_name("li")

for p in produce_lists:
    produce_title = has_ElementExist_h5(p)
    if produce_title != None:
        print("title: %s" % produce_title)
for pn in page_number:
    url = get_next_page(pn)
    print(url)
"""

"""
for list in produce_lists:

        # 商品名称
        produce_title = has_ElementExist_h5(list)
        if produce_title != None:
            print("title: %s" % produce_title)

            for sort in produce_sorts:
                # 商品类别
                produce_sort = has_ElementExist_sort(list,sort)
                if produce_sort != None:
                    print("sort: %s" %produce_sort.text)
                    if sort == produce_sorts[0]:
                            #商品价格
                            produce_price = list.find_element_by_tag_name("span").text
                            print("price: %s" %produce_price)

                            #图片地址
                            produce_pic = list.find_element_by_tag_name("img").get_attribute('src')
                            print("Picture: %s" % produce_pic)
                           # download_pic(produce_price,produce_pic)

            #商品网站
            produce_web = list.find_element_by_tag_name("a").get_attribute("href")
            print('网站：%s' % produce_web)

"""


""" 
#data = driver.find_element_by_id('feed-main-list')
data = driver.find_element_by_class_name('feed-block-title').text
print(data)

print('begin scroll to get info page...')
t1 = time.time()
n = 1   #这里可以控制网页滚动距离
for i in range(1,n+1):
    s = "window.scrollTo(0,document.body.scrollHeight/{0}*{1});".format(n,i)
    #输出滚动位置，网页大小，和时间
    print (s, len(driver.page_source),time.time()-t1)
    driver.execute_script(s)
    time.sleep(1)


data2 = driver.find_element_by_id('J_feed_pagenation').find_element_by_tag_name('li').text
print(data2)
"""

