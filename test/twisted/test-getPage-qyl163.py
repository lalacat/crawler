from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
import time
from bs4 import BeautifulSoup
from urllib.parse import quote


headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
def print_qyl163_content(lis,u):
    urls = list()
    num = 0
    #print("print:%s"%u)
    for l in lis:
        result = dict()
        try:
            href_temp = l.a.get("href")
            result["href"] = "http://www.qyl63.com" + href_temp
            result["title"] = l.a.get("title")
            result["img"] = l.a.div.img.get("src")
            u = result["href"]
            #解决url中带有中文字符
            _us = quote(u).replace("%3A",":")
            child_web = getPage(_us.encode("utf-8"))
            child_web.addCallback(add_video_url,result)
            child_web.addCallback(print_dic,num)
            num += 1
            urls.append(child_web)
        except Exception as e :
            print(e)
    dd = DeferredList(urls)
    dd.addCallback(print_len)
    return dd

def add_video_url(child_page,result):
    try:
        bs_obj = BeautifulSoup(child_page, "html.parser")
        video_url = bs_obj.find('div', id='player-container').video.source.get("src")
        result["video_url"] = video_url
    except Exception as e :
        print(e,result)
    return result


def get_qyl163_content(content):
    try:
        bs_obj = BeautifulSoup(content,"html.parser")
        ul = bs_obj.find("ul","videos")
        lis = ul.find_all("li")
    except Exception as e :
        print(e)

    return lis



def print_len(context):
    print(len(context))
    #print(context)

def print_dic(context,num):
    print(str(num),context)

def finish(context):
    print("finish")
    return None


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
    url = "http://www.qyl63.com/recent/"
    u = "http://www.qyl63.com/recent"


    t1 = time.time()

    

    result = list()
    for i in range(2,5):
        i = str(i)
        u = url + i
        print(u)
        d = read_url(u)
        result.append(d)

    #d = read_url(u)
    dd = defer.DeferredList(result)
    dd.addBoth(lambda _:reactor.stop())



    reactor.run()
    end =time.clock()
    print("运行时间%3.2f"%(end-start))