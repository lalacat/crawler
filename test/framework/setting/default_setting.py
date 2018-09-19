#A
#B

#C
CONCURRENT_REQUESTS = 50 # 设置的并发数(最大下载数)
CONCURRENT_REQUESTS_PER_IP = 0  # ip并发度:
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # 设置HTTPConnectionPool最大保持连接个数
CONCURRENT_ITEMS = 100 #  控制同时处理的爬取到的item的数据数目
#D
DOWNLOADER = "test.framework.downloads.Downloader"
# 默认下载器
DOWNLOAD_HANDLER = "test.framework.downloads.download_agent_redirect.HTTPDownloadHandler"
DOWNLOAD_TIMEOUT = 180      # 3mins

DOWNLOAD_MAXSIZE = 1024*1024*1024   # 1024m 下载网页大小的最大值
DOWNLOAD_WARNSIZE = 32*1024*1024    # 32m 下载网页大小的警戒值

DOWNLOAD_FAIL_ON_DATALOSS = True

DOWNLOAD_DELAY = 0
DOWNLOADER_MIDDLEWARE_TEST = {
    "test.framework.test.test_middleware.test_process_request_01.Change_Request_Header":10
}
#DOWNLOADER_MIDDLEWARE_TEST = {}


#E
#F
#G
#H
HEADER_COLLECTION =[
    ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"],
    ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"],
    ["Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"],
    ["Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"],
    ["Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"],
    ["Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"],
    ["Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"],
    ["Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"],
    ["Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"],
    ["Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"],
    ["Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"],
    ["Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"],
    ["Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6"],
    ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"],
    ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"],
    ["Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"],
]
#T
ITEM_PIPELINES = {
   # "test.framework.middleware.test_process_item_01.Test_Process_item_A":10
    #"test.framework.pipelines.mongoDB.MongoDB":20,
    #"test.framework.pipelines.print_result.Print_Result":10

}
#J
#K
#L
LOG_FORMATTER = "test.framework.log.logformatter.LogFormatter"

'''
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名|
%(funcName)s 调用日志输出函数的函数名|
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮点数表示|
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数|
%(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s 用户输出的消息
'''
#LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_FORMAT = '%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
#LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_DATEFORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_STDOUT = False
LOG_LEVEL = 'DEBUG'


#M
MONGODB_URL = "127.0.0.1:27017"
MONGODB_NAME = "LianJia"

#N
#O
#P

#Q
#R
REACTOR_THREADPOOL_MAXSIZE = 10
RANDOMIZE_DOWNLOAD_DELAY = True  # 随机延迟
#S
SPIDER_MANAGER_CLASS = "test.framework.objectimport.spiderloader.SpiderLoader"
SCHEDULER = "test.framework.scheduler.test_scheduler.Scheduler"
SPIDER_MIDDLEWARES_TEST = {}
#T
'''
TEST_MIDDLEWARE = {
                   "test.framework.middleware.test_for_add_mw_01.Test_MW_A":300,
                   "test.framework.middleware.test_for_add_mw_01.test_fun_common":320,
                   "test.framework.middleware.test_for_add_mw_01.test_fun_A":750,
                   "test.framework.middleware.test_for_add_mw_02.Test_MW_B":200,
                   "test.framework.middleware.test_for_add_mw_02.test_fun_B":150,
                   "test.framework.middleware.test_for_add_mw_02.test_fun_common":140,
                   "test.framework.middleware.test_for_add_mw_03.Test_MW_C":100,
                   "test.framework.middleware.test_for_add_mw_03.test_fun_C":450,
                   "test.framework.middleware.test_for_add_mw_03.test_fun_common":350,
                 }
TEST_DOWNLOADER_MIDDLEWARE = {
    "test.framework.downloads.test_for_download_middleware_01.Test_MW_D_01":100,
    "test.framework.downloads.test_for_download_middleware_01.test_fun_D_A":200,
    "test.framework.downloads.test_for_download_middleware_01.test_fun_common":150,
    "test.framework.downloads.test_for_download_middleware_02.Test_MW_D_02":160,
    "test.framework.downloads.test_for_download_middleware_02.test_fun_D_B":210,
    "test.framework.downloads.test_for_download_middleware_02.test_fun_common":500,
    "test.framework.downloads.test_for_download_middleware_03.Test_MW_D_03":10,
    "test.framework.downloads.test_for_download_middleware_03.test_fun_D_C":300,
    "test.framework.downloads.test_for_download_middleware_03.test_fun_common":400,

}
'''
TEST_DOWNLOADER_MIDDLEWARE = {}
#U
#V
#W
#X
#Y
#Z





