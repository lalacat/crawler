from twisted.web.client import getPage
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from twisted.internet import reactor,defer
from lxml import etree

pagewebXpath = 'body/div[@id="content"]/div/div[@id="feed-wrap"]/div/div[@class="feed-main-con"]'
ulXpath = "body/div[@id='content']/div/div[@id='feed-wrap']/div/div[@class='feed-main-con']/ul[@id='feed-main-list']"
def read_url(request,xpath):
    #print(request_and_response.decode('utf-8'))
    r_s = etree.HTML(request.decode('utf-8'))
    ul = r_s.xpath(xpath)[0].xpath('./div[@class="feed-pagenation"]/ul/li')
    print(ul)
    return ul

def print_web(ul):
    print("print web")
    for r in ul:
        show = r.xpath('./a/@href')
        if show is not None:
            print(show)

@inlineCallbacks
def find_web_page(url,xpath):
    print("begin find page")
    d = getPage(url.encode('utf-8'))
    print(d)
    d.addCallback(read_url,xpath)
    #d.addCallback(print_web)
    yield d

if __name__ =='__main__':
    d = find_web_page("https://www.smzdm.com",pagewebXpath)
    d.addCallback(lambda _:reactor.stop())

    reactor.run()