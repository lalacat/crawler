from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
#from test.public_api.web import get_need_datas,print_result
import json,time
from bs4 import BeautifulSoup

url = 'https://www.smzdm.com/homepage/json_more?p='
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


def print_qyl163_content(lis,num):
    print("print:%d"%num)
    for l in lis:
        href_temp = l.a.get("href")
        href = "http://www.qyl63.com" + href_temp
        print(href)


def get_qyl163_content(content):
    print("parse")
    try:
        bs_obj = BeautifulSoup(content,"html.parser")

        ul = bs_obj.find("ul","videos")
        lis = ul.find_all("li")

    except Exception as e :
        print(e)
    return lis




@inlineCallbacks
def read_url(url):
    d = getPage(url.encode('utf-8'))
    d.addCallback(get_qyl163_content)
    d.addCallback(print_qyl163_content)
    yield d


if __name__ == '__main__':

    d = read_url("http://www.qyl63.com/recent")
    #reactor.callLater(0,d)
    d.addCallback(lambda _:reactor.stop())
    reactor.run()