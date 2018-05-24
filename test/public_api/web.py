import time,json
from twisted.internet import reactor

def get_need_datas(web_body):
    datas_list = list()
    if isinstance(web_body,bytes):
        web_body = json.loads(web_body)
    if isinstance(web_body,dict):
        if web_body.__contains__("data"):
            datas = web_body['data']
    for d in datas:

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
           # print(p,d)
            pass
    print("==============================")
    return


def end_crawl(_, t_begin):
    t_end = time.time()
    print(t_end - t_begin)
    reactor.stop()
