import sys,os,time,inspect
from twisted.internet import reactor,defer
from twisted.web.client import getPage
from queue import Queue
from pkgutil import iter_modules
from importlib import import_module
from test.public_api.web import MongoDb
from test.spider import BaseSpider,BaseQylSpider


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

            # 如果block为False，如果有空间中有可用数据，取出队列，否则立即抛出Empty异常
            req = self.scheduler.next_request()

            d = getPage(req.url.encode('utf-8'))
            # d.addCallback(self.get_response_callback,req)
            # d.addCallback(self.print_web)
            d.addCallback(req.parse,req.url)
            d.addCallback(db.insert_mongoDb)
            d.addCallback(lambda _:reactor.callLater(0,self._next_request,spider_name,db))

        except Exception as e:
            print(e)

    @defer.inlineCallbacks
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
            # 判断爬虫是否有专用的数据库，数据库的地址，名称在爬虫类中定义
            if hasattr(spider,"db_url"):
                db_url = spider.db_url
            else:
                db_url = "127.0.0.1:27017"
            if hasattr(spider,"db_name"):
                db_name = spider.db_name
            else:
                db_name = "Twisted_Database"
        except Exception as e :
            print(e)

        db = self._create_db(db_url,db_name)
        db.collection_name = spider.name

        yield db.connectDb()
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


class Spider(object):
    def __init__(self,projectName,path="spider"):
        self.projectName = projectName
        self.path = path

    def _spider_module_path(self):
        '''
        将爬虫包附加到系统路径中，只有在系统路径中，模块导入才能被识别到
        :param projectName: 项目名称
        '''

        # 获取文件当前路径
        curent_path = os.getcwd()
        try:
            # 找到项目的根目录的绝对地址，并将工作目录切换到根目录下
            root_direction = curent_path.split(self.projectName)[0] + self.projectName
            # 获取根目录下所有的子文件夹
            listdir = os.listdir(root_direction)
            for l in listdir:
                if l == 'test':
                    temp = os.path.join(root_direction, l)
                    os.chdir(temp)

            sys.path.append(os.getcwd())
        except FileNotFoundError as e:
            print("项目名称错误")

        '''
        #先判断是否有爬虫包的存在
        #存在的话就直接导入包
        #不存在的话就创建一个爬虫包
        if not dirlist.__contains__("spider"):
            os.mkdir("spider")

        '''
    def _import_spider(self):

        # 导入爬虫包
        spider = import_module(self.path)

        spiders = list()
        spiders.append(spider)

        if hasattr(spider, "__path__"):
            print(spider.__path__)

            for _, subpath, ispkg in iter_modules(spider.__path__):
                # 取得模块的绝对路径
                fullpath = self.path + "." + subpath

                # 判断是模块包还是模块
                if ispkg:
                    # 是模块包的话重新调用本方法将模块包下的所以模块都导入
                    spiders += self.import_spider(self,fullpath)
                else:
                    # 是模块的话就直接导入到结果中
                    submod = import_module(fullpath)
                    spiders.append(submod)
        else:
            print("路径不对，脚本放在根目录下")
        return spiders

    def _get_spider(self):
        self._spider_module_path()
        spiders = self._import_spider()

        for c in spiders:
            for obj in vars(c).values():
                """
                vars（）实现返回对象object的属性和属性值的字典对象
                要过滤出obj是类的信息，其中类的信息包括，模块导入其他模块的类的信息，模块中的父类，模块中所有定义的类
                因此，条件过滤分别是：
                1.判断obj的类型为class
                2.判断是否继承父类，因此命令包中__init__文件中定义的就是整个包中所需要的父类
                3.判断类是否为模块本身定义的类还是导入其他模块的类(感觉第二个条件包含此条件了有些多余)
                4.剔除父类
                """
                if inspect.isclass(obj) and \
                        issubclass(obj, BaseQylSpider) and \
                        obj.__module__ == c.__name__ and \
                        getattr(obj,'name', None) and \
                        not obj == BaseSpider:
                    yield obj


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