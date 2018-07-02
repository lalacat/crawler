
from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
#from test.public_api.web import get_need_datas,print_result
import json,time
from bs4 import BeautifulSoup
from twisted.protocols.sip import URL
from twisted.python.urlpath import  URLPath
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


def print_qyl163_content(lis,u):
    urls = list()
    print("print:%s"%u)
    for l in lis:
        result = dict()
        try:
            href_temp = l.a.get("href")
            result["href"] = "http://www.qyl63.com" + href_temp
            result["title"] = l.a.get("titile")
            result["img"] = l.a.div.img.get("src")
            u  =  result["href"]

            #解决url中带有中文字符
            us = URLPath.fromString(u)
            child_web = getPage(us.path)

            #child_web.addCallBack(add_video_url,result)
            urls.append(child_web)
        except Exception as e :
            print(e)
    return DeferredList(urls)

def add_video_url(child_page,result):
    print("add url")
    try:
        bs_obj = BeautifulSoup(child_page, "html.parser")
        video = bs_obj.find("video", "player_html5_api")
        url = video.get("src")
        result["video_url"] = url
    except Exception as e :
        print(e)
    return None


def get_qyl163_content(content):
    print("parse")
    try:
        bs_obj = BeautifulSoup(content,"html.parser")
        ul = bs_obj.find("ul","videos")
        lis = ul.find_all("li")

    except Exception as e :
        print(e)

    return lis



def print_web(context):
    print("print_web")
    print(context)


def finish(context):
    print("finish")
    print(context)



@inlineCallbacks
def read_url(url):
    d = getPage(url.encode('utf-8'))
    try:
        d.addCallbacks(get_qyl163_content)
        d.addCallback(print_qyl163_content,url)
        d.addCallback(finish)
    except Exception as e :
        print(e)


    yield d



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
    #d.addCallback(lambda _:reactor.stop())

    reactor.run()
    end =time.clock()
    print("运行时间%3.2f"%(end-start))