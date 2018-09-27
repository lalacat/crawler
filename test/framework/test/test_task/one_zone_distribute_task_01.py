import queue

from twisted.internet import task, reactor

from test.framework.test.test_spider.simple_spider_getPage_01 import SimpleSpider

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


spider01 = SimpleSpider()
spider02 = SimpleSpider()
spider03 = SimpleSpider()

unactived_spider = [spider01,spider02,spider03]


def spider_has_task(spider):
    return spider.start_urls



def check_spider_task(unactived_spider):
    for spider in unactived_spider:
        if not spider_has_task(spider):
            spider.start_urls = top_task.get(block=False)
            spider.name = spider.start_urls[0].split('/')[-2]
            unactived_spider.remove(spider)




def next_task():
    if top_task.qsize()>0:
        try:
            check_spider_task(unactived_spider)
        except Exception :
            print("have no task")
    for i in unactived_spider:
        print(i.name)
        i.start_requests()

if __name__ == "__main__":
    long_task = task.LoopingCall(next_task)
    long_task.start(3)
    reactor.run()


