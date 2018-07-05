import logging

logger = logging.getLogger(__name__)

class LogCounterHandler(logging.Handler):
    """Record log levels count into a crawler stats"""

    def __init__(self, crawler, *args, **kwargs):
        super(LogCounterHandler, self).__init__(*args, **kwargs)
        self.crawler = crawler

    #每进行一次log.info就会调用这个方法，从而可以计算出调用多少次
    def emit(self, record):
        sname = 'log_count/{}'.format(record.levelname)
        self.crawler.inc_value(sname)

class Crawler(object):
    def __init__(self):
        self.stats = dict()

    def inc_value(self, key, count=1, start=0, spider=None):
        d = self.stats
        d[key] = d.setdefault(key, start) + count

if __name__ == "__main__":
    c = Crawler()
    handler= LogCounterHandler(c,level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.root.addHandler(handler)

    logging.info('this is 1 loggging info message')
    logging.info('this is 2 loggging info message')
    logging.info('this is 3 loggging info message')

    print(c.stats)
