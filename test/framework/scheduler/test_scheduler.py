import logging

import queue
logger = logging.getLogger(__name__)

class Scheduler(object):

    def __init__(self,mqclass=None):
        self.mqs = mqclass # 内存任务队列类FIFO

    @classmethod
    def from_crawler(cls,crawler=None):
        #setting = crawler.settings
        mqs = queue.Queue()

        return cls(mqclass=mqs)

    def has_unhandler_requests(self):
        return len(self) > 0

    def open(self,spider):
        logger.info("数据队列已准备")
        self.spider = spider
        #self.mqs = self._newfifo()
        return

    def next_request(self):
        logger.debug("取下一个数据。。。")
        # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
        try:
            requset = self.mqs.get(block=False)
        except Exception as e:
            logger.debug("队列数据已取完")
            requset = None
        return requset

    def _mqpush(self,requset):
        self.mqs.put(requset)

    def __len__(self):
        return self.mqs.qsize()

    def _newfifo(self):
        return self.mqclass



class RFPDupeFilter():
    pass