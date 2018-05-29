from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer,task
from twisted.web.client import getPage
from twisted.web.http_headers import Headers
from lxml import etree

urls = {1:"https://www.smzdm.com/p2/" ,
        2:"https://www.smzdm.com/p4/" ,
        3:"https://www.smzdm.com/p5/" ,
        4:"https://www.smzdm.com/homepage/json_more?p=0"}

header = Headers({'User-Agent':['MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'],
                  'content-type':["application/json"]})

def read_url(request):
    #print(request.decode('utf-8'))
    r_s = etree.HTML(request.decode('utf-8'))
    ul = r_s.xpath("body/div[@id='content']/div/div[@id='feed-wrap']/div"
                     "/div[@class='feed-main-con']/ul[@id='feed-main-list']")[0].xpath('./li')
    return ul

def print_web(ul,id):
    print("print web %d"%id)
    for r in ul:
        show = r.xpath('./h5/a/@href')
        if show is not None:
            print(show)
    return


@inlineCallbacks
def spider_web(url,id):
    print("start %d job"%id)
    d = getPage(url.encode('utf-8'),headers=header)
    print(d)
    d.addCallback(read_url)
    d.addCallback(print_web,id)
    yield d

li = []
for id,url in urls.items():
    print(url)
    d = spider_web(url,id)
    li.append(d)

dd = defer.DeferredList(li)
dd.addBoth(lambda _ : reactor.stop())
reactor.run()