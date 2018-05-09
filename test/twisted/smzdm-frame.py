from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
import requests
from lxml import etree

urls = ["https://www.smzdm.com/p2/",
       "https://www.smzdm.com/p4/" ,
        "https://www.smzdm.com/p5/"]
header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

def request(url):
    result = requests.get(url,headers=header)
    return result

def read_url(request):
    r_s = etree.HTML(request.text)
    ul = r_s.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                     "/div[@class='feed-main-con']/ul[@id='feed-main-list']")[0].xpath('./li')
    return ul

def print_web(ul):
    for r in ul:
        show = r.xpath('./h5/a/@href')
        if show is not None:
            print(show)
    return

@inlineCallbacks
def spider_web(url,id):
    print("start %d job"%id)
    d = Deferred()