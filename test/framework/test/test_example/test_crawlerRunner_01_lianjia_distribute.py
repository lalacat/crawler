import queue

from twisted.internet import reactor

from test.framework.setting import Setting
from test.framework.test.test_crawler.test_crawlerRunner import CrawlerRunner

zone_name = "yangpu"
town_urls = [
    'https://sh.lianjia.com/xiaoqu/anshan/',
    'https://sh.lianjia.com/xiaoqu/dongwaitan/',
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/'
]

top_task = queue.Queue()
for url in town_urls:
    top_task.put(url)

def spider_has_task(spider):
    return spider.start_urls


s = Setting()
cr = CrawlerRunner(top_task,s)
cr.start()
reactor.run()

