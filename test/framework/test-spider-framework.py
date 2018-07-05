from twisted.internet import reactor,defer
from twisted.web.client import getPage
from queue import Queue
from test.public_api.web import MongoDb
from urllib.parse import quote
from test.framework.import_spider import Spider
import time
from twisted.python import log


class HttpResponse(object):

    def __init__(self,context,request):
        self.content = context
        self.request = request
        self.url = request.url
        self.text = request.parse(context,self.url)


class Scheduler(object):
    """
    任务调度器
    """
    def __init__(self,name):
        self.q = Queue()
        self.name = name

    def open(self):
        print("爬虫：%s 已载入" %self.name)

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

    @staticmethod
    def get_response_callback(content, request):
        print("get_response_callback")
        web_response = HttpResponse(content, request)
        return web_response.text

    def _next_request(self,spider_name="default_task",db=None):
        '''
        :param kargs: name ,
        :return:
        '''
        if self.scheduler.qsize() != 0 :
            print("爬虫：%s 还剩下%d个网页"%(spider_name,self.scheduler.qsize()))

        try:
            if self.scheduler.qsize() == 0 and len(self.crawlling) == 0:
                print("爬虫 %s end"%spider_name)
                self._close.callback(None)
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
            print("AttributeError",e)
            return None
        except Exception as e :
            print("Exception",e)


    #当一个defer爬虫结束后，将完成的爬虫线程从list中移除去
    def finish_crawl(self,content,req):
        print("finish")
        self.crawlling.remove(req)
        return content

    def crawl_err(self,content):
        print("error found")
        print(content)
        return "error"

    @defer.inlineCallbacks
    #将爬虫中的网页读取出来
    def open_spider(self,spider,db=None):
        self.scheduler = Scheduler(spider.name)
        yield self.scheduler.open()
        start_requests = iter(spider.start_requests())
        while True:
            try:
                req = next(start_requests)
                print("读取网站:%s"%req.url)
            except StopIteration as e:
                print("网站读取完毕")
                break
            except Exception as e :
                print(e)
            self.scheduler.enqueue_request(req)
        reactor.callLater(0,self._next_request,spider.name,db)

    @defer.inlineCallbacks
    def start(self):
        self._close = defer.Deferred()
        yield self._close


class Crawler(object):
    """
    用户封装调度器以及引擎的...
    """
    def _create_engine(self):
        print("爬虫引擎已创建")
        return ExecutionEngine()

    def _create_spider(self,spider):
        print("爬虫：%s 已创建" %spider.name)
        return spider()

    def _create_db(self,db_url,db_name):
        print("数据库已创建")
        return MongoDb(db_url,db_name)

    @defer.inlineCallbacks
    def crawl(self,spider):
        engine = self._create_engine()
        spider = self._create_spider(spider)
        try:
            if hasattr(spider,"db_flag"):
                if spider.db_flag:
                    # 判断爬虫是否有专用的数据库，数据库的地址，名称在爬虫类中定义
                    if hasattr(spider,"db_url"):
                        db_url = spider.db_url
                    else:
                        db_url = "127.0.0.1:27017"
                    if hasattr(spider,"db_name"):
                        db_name = spider.db_name
                    else:
                        db_name = "Twisted_Database"
                    db = self._create_db(db_url, db_name)
                    db.collection_name = spider.name
                    yield db.connectDb()
                else:
                    print("此爬虫不关联数据库")
                    db = None
        except Exception as e :
            print(e)


        yield engine.open_spider(spider,db)
        yield engine.start()


class CrawlerProcess(object):
    """
    开启事件循环
    """
    def __init__(self):
        self._active = set()

    def crawl(self,spider):
        """
        :param spider_cls_path:
        :return:
        """
        crawler = Crawler()
        d = crawler.crawl(spider)
        self._active.add(d)

    def start(self):
        dd = defer.DeferredList(self._active)
        dd.addBoth(lambda _:reactor.stop())
        reactor.run()




class Commond(object):
    def __init__(self):
        pass

    def run(self):
        crawl_process = CrawlerProcess()
        spider = Spider("crawler")
        for spider_cls_path in spider._get_spider():
            crawl_process.crawl(spider_cls_path)
        crawl_process.start()


if __name__ == "__main__":
    start = time.clock()
    cmd = Commond()
    cmd.run()
    end = time.clock()
    print("运行时间%3.2f"%(end-start))