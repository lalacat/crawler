import pprint

from twisted.internet import defer

from test.framework.core.crawlerRunner import CrawlerRunner
from test.framework.test.test_example.mutil_sold_info.child_spider_sold_xpath import CollectSold


class Spider_Out_print(object):
    def __init__(self,settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    @defer.inlineCallbacks
    def close_spider(self,spider):
        try:
            # print("%s 理论获取小区数为%d个"%(spider.name,int(spider.result["total_xiaoqu_number"][0])))
            if hasattr(spider,'output'):
                if spider.output:
                    # print(pprint.pformat(spider.result))
                    if hasattr(spider,'sold_url'):
                        print((pprint.pformat(spider.sold_url)))
                        cr = CrawlerRunner(spider.sold_url, spider.settings, CollectSold, name=spider.name,
                                           logformat=spider.lfm, middlewares=spider.crawler.middlewares)
                        yield cr.start()
        except Exception as e :
            print("Spider_Out_print",e)

        yield None
