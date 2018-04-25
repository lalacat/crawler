from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
url = "https://www.kaistart.com/project/more.html"
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = "MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"
#browser = webdriver.PhantomJS(desired_capabilities=dcap)
browser = webdriver.Chrome()
browser.maximize_window()
browser.get(url)
js1 = "window.scrollTo(0,document.body.scrollHeight)"
js2 = "return document.body.scrollHeight"
n = 0
browser.execute_script(js1)
old_hight = browser.execute_script(js2)
new_hight = old_hight
while new_hight >= old_hight:
    #browser.save_screenshot('.\\pic\\debug.png')
    n= n+1
    old_hight = browser.execute_script(js2)
    print("第%d次滚动: %d " %(n,old_hight))
    browser.execute_script(js1)
    new_hight = browser.execute_script(js2)
    time.sleep(0.7)

program_list = browser.find_elements_by_class_name("programCard")

print(len(program_list))
"""
for p_l in program_list:
    title = p_l.find_element_by_class_name("title").text
    print(title)

"""