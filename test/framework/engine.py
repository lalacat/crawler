from twisted.internet import defer,reactor
from twisted.web.client import getPage
from queue import Queue
from urllib.parse import quote

import logging

logger = logging.getLogger(__name__)


class Scheduler(object):
    """
    任务调度器
    """
    def __init__(self,name):
        self.q = Queue()
        self.name = name

    def open(self):
        logger.info("爬虫：%s 已载入" %self.name)

    def next_request(self):
        # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
        try:
            req = self.q.get(block=False)
        except Exception as e:
            req = None
        return req

    def enqueue_request(self,req):
        self.q.put(req)

    def qsize(self):
        return self.q.qsize()


class ExecutionEngine(object):
    """
    引擎：所有调度
    """

    def __init__(self):
        #print("引擎初始化")
        self._close = None
        self.scheduler = None
        #self.max = 5
        #保证每个defer都执行完
        self.crawlling = []



    def _next_request(self,spider_name="default_task",db=None):
        '''
        :param kargs: name ,
        :return:
        '''
        if self.scheduler.qsize() != 0 :
            logger.info("爬虫：%s 还剩下%d个网页"%(spider_name,self.scheduler.qsize()))

        try:
            if self.scheduler.qsize() == 0 and len(self.crawlling) == 0:
                logger.info("爬虫 %s end"%spider_name,exc_info=True,extra={'spider': spider_name})
                self._finish_stopping_engine()
                return

            req = self.scheduler.next_request()
            #对即将处理的req存储到临时列表中，这是为了防止其他的req还没处理完，程序就结束了，因为判断程序结束的标志时scheduler的q.size()为0，
            #即任务队列中的数据全部取出来了，但是结束标志中还需要在定义一个标志，表示所有的defer都处理完了，就用crawlling进行处理，任务进行前，
            #先将要进行的任务存储到crawlling列表中，当数据处理完，再将对应的req从列表中去除，当列表为空的时候，证明所有的defer的callback处理完了
            self.crawlling.append(req)
            # 对网页进行编码的处理，防止网页中含有中文字符，程序不能对中文字符进行解析，报错；
            # 对网页进行处理后‘：’也会被解析成“%3A”，所以要对解析后的网页在进行处理将“：”重新代替回来
            _url = quote(req.url).replace("%3A",":")
            d = getPage(_url.encode('utf-8'))


            # d.addCallback(self.get_response_callback,req)
            # d.addCallback(self.print_web)

            d.addCallback(req.parse,req.url)
            d.addCallback(self.finish_crawl, req)
            if db is not None:
                d.addCallback(db.insert_mongoDb)

            d.addErrback(self.crawl_err)
            d.addBoth(lambda _:reactor.callLater(0,self._next_request,spider_name,db))

        except AttributeError as e:
            logger.error("对象没有对应的属性",e)
            return None
        except Exception as e :
            logger.error("Exception",e)


    #当一个defer爬虫结束后，将完成的爬虫线程从list中移除去
    def finish_crawl(self,content,req):
        logger.info("finish")
        self.crawlling.remove(req)
        return content

    def crawl_err(self,content):
        print("error found")
        print(content)
        return "error"

    @defer.inlineCallbacks
    #将爬虫中的网页读取出来
    def open_spider(self,spider,db=None):
        logger.info("分解spider")
        self.scheduler = Scheduler(spider.name)
        yield self.scheduler.open()
        start_requests = iter(spider.start_requests())
        while True:
            try:
                req = next(start_requests)
                logger.info("读取网站:%s"%req.url)
            except StopIteration as e:
                logger.error("网站读取完毕")
                break
            except Exception as e :
                logger.error("再对spider操作的过程中出现错误",e)
            self.scheduler.enqueue_request(req)
        reactor.callLater(0,self._next_request,spider.name,db)

    @defer.inlineCallbacks
    def start(self):
        self._close = defer.Deferred()
        yield self._close

    def  _finish_stopping_engine(self):
        self._close.callback(None)