from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from test.public_api.web import get_need_datas,print_result
import json
url = 'https://www.smzdm.com/homepage/json_more?p='
headers = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

def get_need_datas(datas):
    print(datas)
    datas_list = list()
    temp = json.loads(datas)
    #print(type(temp))
    #print(temp)
    #print()
    print(type(temp["data"]))
    produce = temp["data"]
    print(type(produce[0]))

    for k in produce:

        #print(k)
        pass
    '''
    '''

    for d in produce:
        result = dict()
        #Python 3.X 里不包含 has_key() 函数，被 __contains__(key) 替代:
        #标签是：z-tag-zixun 没有article_price，article_link，top_category

        if d.__contains__("article_id"):
            result["article_id"] = d["article_id"]
            if d.__contains__("article_title"):
                result["article_title"] = d["article_title"]

            if d.__contains__("article_price"):
                result["article_price"] = d["article_price"]

            if d.__contains__("article_mall"):
                result["article_mall"] = d["article_mall"]

            if d.__contains__("article_pic"):
                result["article_pic"] = d["article_pic"]

            if d.__contains__("article_link"):
                result["article_link"] = d["article_link"]

            if d.__contains__("article_url"):
                result["article_url"] = d["article_url"]

            if d.__contains__("article_channel_class"):
                result["article_channel_class"] = d["article_channel_class"]

            if d.__contains__("top_category"):
                result["top_category"] = d["top_category"]
            datas_list.append(result)

    return datas_list


def print_result(datas_list,url):
    print("页面 :%s 有 %d 件商品"%(url,len(datas_list)))
    for d_l in datas_list:
        for p,d in d_l.items():
            print(p,d)
    print("==============================")
    return


@inlineCallbacks
def read_url(url):
    print("begin find page")
    d = getPage(url.encode('utf-8'))
    print(d)
    d.addCallback(get_need_datas)
    d.addCallback(print_result,url)

    yield d


if __name__ == '__main__':
    result = list()
    for i in range(1):
        i = str(i)
        u = url + i
        print(u)
        d = read_url(u)
        result.append(d)

    dd = defer.DeferredList(result)
    dd.addBoth(lambda _:reactor.stop())
    reactor.run()