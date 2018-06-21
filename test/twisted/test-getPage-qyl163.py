from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
#from test.public_api.web import get_need_datas,print_result
import json,time
from bs4 import BeautifulSoup

url = 'https://www.smzdm.com/homepage/json_more?p='
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


def print_qyl163_content(lis,url):
    print("print:%s"%url)
    for l in lis:
        result = dict()
        href_temp = l.a.get("href")
        result["href"] = "http://www.qyl63.com" + href_temp
        result["title"] = l.a.get("titile")
        result["img"] = l.a.div.img.get("src")
        print(result["href"])
        child_web = getPage(result["href"].encode("utf-8"))
        child_web.addCallBack(lambda _:print("child page"))
        #esult["video"]= child_web.addCallback()
        #print(img)


def get_qyl163_content(content):
    print("parse")
    try:
        bs_obj = BeautifulSoup(content,"html.parser")
        ul = bs_obj.find("ul","videos")
        lis = ul.find_all("li")

    except Exception as e :
        print(e)

    return lis

def get_qyl_video(child_page):
    bs_obj = BeautifulSoup(child_page, "html.parser")
    video = bs_obj.find("video", "player_html5_api")
    returnValue(video)

def print_web(context):
    print("print_web")
    print(context)

@inlineCallbacks
def read_url(url):
    d = getPage(url.encode('utf-8'))

    #d.addCallback(print_web)
    d.addCallback(get_qyl163_content)
    d.addCallback(print_qyl163_content,url)

    yield d

@inlineCallbacks
def read_child_url(url):
    pass

if __name__ == '__main__':
    start = time.clock()
    """
    t1 = time.time()
    result = list()
    for i in range(3):
        i = str(i)
        u = url + i
        d = read_url(u)
        result.append(d)

    
    dd = defer.DeferredList(result)
    dd.addBoth(lambda _:reactor.stop())

    
    """
    url = "http://www.qyl63.com/recent"

    d = read_url(url)
    d.addCallback(lambda _:reactor.stop())
    reactor.run()
    end =time.clock()
    print("运行时间%3.2f"%(end-start))