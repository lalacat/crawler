from spider import BaseSpider,Request,BaseQylSpider,Spider
from bs4 import BeautifulSoup
from twisted.python import failure
from urllib.parse import quote
from twisted.web.client import getPage

from twisted.internet.defer import DeferredList

class QylSpider(BaseQylSpider):
    name = "QYL-1"
    url =  "http://www.qyl63.com/recent/"
    db_name = "QYL"
    db_flag = True
    def __init__(self):
        #self.q = queue.Queue()
        self.num = 0

    def start_requests(self):
        start_url = list()

        for i in range(3):
            if i < 1:
                u = self.url
            elif i > 1 :
                i = str(i)
                u = self.url + i
            start_url.append(u)

        self. num = start_url.__len__()

        for url in start_url:
            yield Request(url,self._parse)

    def _parse(self,context, url):
        print("解析网页：", url)
        try:
            lists = self._qyl163_items(context)
            results = self._item_dicts(lists)
        except Exception as e:
            print(e)
        return results

    #获取recent页面的视频列表
    def _qyl163_items(self,content):
        try:
            bs_obj = BeautifulSoup(content,"html.parser")
            ul = bs_obj.find("ul","videos")
            lis = ul.find_all("li")
        except Exception as e :
            print(e)

        return lis

    #对列表中的每一项进行解析，获取需要的元素
    def _item_dicts(self,lis):
        urls = list()
        num = 0
        for l in lis:
            result = dict()
            try:
                href_temp = l.a.get("href")
                result["href"] = "http://www.qyl63.com" + href_temp
                result["title"] = l.a.get("title")
                result["img"] = l.a.div.img.get("src")
                u = result["href"]
                # 解决url中带有中文字符
                _us = quote(u).replace("%3A", ":")
                video_page = getPage(_us.encode("utf-8"))
                video_page.addCallback(self._find_video_download, result)
                video_page.addCallback(self._print_dic, num)
                num += 1
                urls.append(video_page)
            except Exception as e:
                print(e)
        dd = DeferredList(urls)
        dd.addCallback(self._deal_final_result)
        return dd

    #获取子页面视频下载的地址
    def _find_video_download(self,child_page,result):
        try:
            bs_obj = BeautifulSoup(child_page, "html.parser")
            video_url = bs_obj.find('div', id='player-container').video.source.get("src")
            result["video_url"] = video_url
        except Exception as e :
            return failure.Failure(e)
            #print(e,result)
        return result

    def _print_dic(self,context, num):
        #print(str(num), context)
        return context

    def _deal_final_result(self,content):
        #print(len(content))
        #print(type(content))
        result = list()
        for c in content:
            result.append(c[1])
        return result