from twisted.internet import defer,reactor
from twisted.web.client import getPage
from queue import Queue
from urllib.parse import quote
from test.framework.url_convert import safe_url_string
import logging,time


LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT)
logger = logging.getLogger(__name__)

class ExecutionEngine(object):
    """
    引擎：所有调度
    """

    def __init__(self,crawler,spider_closed_callback):
        logger.debug("引擎初始化")
        self.crawler =crawler
        self.settings = crawler.settings
        #获取log的格式
        self.logformatter = crawler.logformatter

        self.running = False
        self._close = None
        self.scheduler = None
        #self.max = 5
        #保证每个defer都执行完
        self.crawlling = []


    @defer.inlineCallbacks
    def start(self):
        assert not self.running,"引擎已启动"
        self.start_time = time.time(2.3)
        print(self.start_time)
        logger.debug("engine start: %{time}r",{'time':self.start_time})

        print("kaishi")
        #yield 信号处理
        self.running = True


        self._closewait = defer.Deferred()
        yield self._closewait


    def stop(self):
        logger.info("stop")
        self._close.callback(None)

    def _next_request(self,spider_name="default_task",db=None):
        '''
        :param kargs: name ,
        :return:
        '''
        if self.scheduler.qsize() != 0 :
            logger.info("爬虫：%s 还剩下%d个网页"%(spider_name,self.scheduler.qsize()))

        try:

            if self.scheduler.qsize() == 0 and len(self.crawlling) == 0:
                logger.info("爬虫 %s end"%spider_name)
                self._finish_stopping_engine()
                return


            req = self.scheduler.next_request()
            #if req is not None:
            #对即将处理的req存储到临时列表中，这是为了防止其他的req还没处理完，程序就结束了，因为判断程序结束的标志时scheduler的q.size()为0，
            #即任务队列中的数据全部取出来了，但是结束标志中还需要在定义一个标志，表示所有的defer都处理完了，就用crawlling进行处理，任务进行前，
            #先将要进行的任务存储到crawlling列表中，当数据处理完，再将对应的req从列表中去除，当列表为空的时候，证明所有的defer的callback处理完了
            self.crawlling.append(req)
            # 对网页进行编码的处理，防止网页中含有中文字符，程序不能对中文字符进行解析，报错；
            # 对网页进行处理后‘：’也会被解析成“%3A”，所以要对解析后的网页在进行处理将“：”重新代替回来
            #_url = quote(req.url).replace("%3A",":")
            #print(_url)
            _url = safe_url_string(req.url,"utf-8")

            d = getPage(_url.encode('utf-8'))


            # d.addCallback(self.get_response_callback,req)
            #d.addCallback(self.print_web)

            d.addCallback(req.parse,req.url)
            d.addCallback(self.finish_crawl, req)
            if db is not None:
                d.addCallback(db.insert_mongoDb)

            d.addErrback(self.crawl_err,req)
            d.addBoth(lambda _:reactor.callLater(0,self._next_request,spider_name,db))

        except AttributeError as e:
            logger.error("对象没有对应的属性",e)
            return None
        except Exception as e :
            logger.error("Exception",e)

    def print_web(self,content):

        for items in content:
            for key,value in items.items():
                print(key,value)


    #当一个defer爬虫结束后，将完成的爬虫线程从list中移除去
    def finish_crawl(self,content,req):
        logger.info("finish")
        self.crawlling.remove(req)
        return content

    def crawl_err(self,content,req):
        logger.error("error found \n",content)
        self.crawlling.remove(req)
        return None


    @defer.inlineCallbacks
    #将爬虫中的网页读取出来
    def open_spider(self,spider,start_requests,db=None):
        logger.info("分解spider")
        yield self.scheduler.open()
        while True:
            try:
                req = next(start_requests)
                logger.info("读取网站:%s"%req.url)
            except StopIteration as e:
                logger.info("网站读取完毕")
                break
            except Exception as e :
                logger.error("在对spider网页导入的操作的过程中出现错误",e)
            self.scheduler.put_request(req)


    def  _finish_stopping_engine(self):
        logger.info("finish")
        self._close.callback(None)

