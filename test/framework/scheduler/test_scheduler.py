import logging

import queue
logger = logging.getLevelName(__name__)

class Scheduler(object):

    def __init__(self,mqclass=None):
        self.mqclass = mqclass # 内存任务队列类FIFO

    @classmethod
    def from_crawler(cls,crawler):
        #setting = crawler.settings
        mqclass = queue.Queue()
        return cls(mqs=mqclass)

    def has_unhandler_request(self):
        return len(self)>0

    def open(self,spider):
        logger.info("数据队列已准备")
        self.spider = spider
        self.mqs = self._newfifo()
        return

    def __len__(self):
        return len(self.mqs)

    def _newfifo(self):
        return self.mqs()


class RFPDupeFilter():
    pass