#A
#B

#C
CONCURRENT_REQUESTS = 10 # 设置的并发数(最大下载数)
CONCURRENT_REQUESTS_PER_IP = 0  # ip并发度:
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # 设置HTTPConnectionPool最大保持连接个数
CONCURRENT_ITEMS = 100 #  控制同时处理的爬取到的item的数据数目
#D
DOWNLOADER = "test.framework.downloads.Downloader"
# 默认下载器
DOWNLOAD_HANDLER = "test.framework.downloads.download_agent_proxy.HTTPDownloadHandler"
DOWNLOAD_TIMEOUT = 180    # 3mins

DOWNLOAD_MAXSIZE = 1024*1024*1024   # 1024m 下载网页大小的最大值
DOWNLOAD_WARNSIZE = 32*1024*1024    # 32m 下载网页大小的警戒值

DOWNLOAD_FAIL_ON_DATALOSS = True

DOWNLOAD_DELAY = 0
DOWNLOADER_MIDDLEWARE = {
    "test.framework.downloads.download_middleware.user_agent.ChangeRequestUserAgent":10,
   #  如果使用chang proxy 必须放在add http proxy 这个类前面执行，否则会报错
   "test.framework.downloads.download_middleware.change_proxy.ChangeProxy": 20,
   "test.framework.downloads.download_middleware.http_proxy.AddHttpProxy": 30,
   "test.framework.downloads.download_middleware.record_download_errurl.RecordDownloadErrorUrl": 40,

}
DOWNLOAD_TCP_TIMEOUT_MAX_TIMES = 6
DOWNLOAD_TIMEOUT_MAX_TIMES =4

#E
#F
#G
#H
# HEADER_COLLECTION =[
#     ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"],
#     ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"],
#     ["Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"],
#     ["Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"],
#     ["Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"],
#     ["Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"],
#     ["Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"],
#     ["Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"],
#     ["Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"],
#     ["Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"],
#     ["Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"],
#     ["Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"],
#     ["Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6"],
#     ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"],
#     ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"],
#     ["Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"],
# ]
HEADER_COLLECTION = [
    # Firefox
    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'],
    ["Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0"],
    ['Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'],
    # Chrome
    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'],
    ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'],
    ['Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'],
    ['Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko'],
    ['Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)'],
    # Opera
    ['Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52'],
    ['Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62'],
    # Safari
    ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'],
    ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'],

    # Bot
    ['Googlebot/2.1 (+http://www.googlebot.com/bot.html)'],
    ['Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'],
    ['Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)']
]
HTTPPROXY_AUTH_ENCODING = 'utf-8'

#T
ITEM_PIPELINES = {
    # "test.framework.pipelines.mongoDB.MongoDB":20,
    # "test.framework.test.test_middleware.test_db.lianjia_xiaoqu_mongoDB_01.LJ_XQ_DB":10,
    # "test.framework.test.test_middleware.test_db.mutil_sold.LJ_Sold_DB":10,
    # "test.framework.pipelines.print_result.Print_Result":10,
    # "test.framework.test.test_middleware.test_close_spider_print_01.test_print.Spider_Out_print": 10,
    # "test.framework.test.test_middleware.test_close_spider_print_02_lianjia_xiaoqu.test_print.Spider_Out_print": 10,
    # "test.framework.test.test_middleware.test_close_spider_print_03_lianjia_xiaoqu_db.test_print.Spider_Out_print": 10,
    # "test.framework.test.test_middleware.test_itempipe_collection_info.Collection_print": 20,
    # "test.framework.test.test_middleware.test_print.test_close_spider_print_04_lianjia_xiaoqu_house.Spider_Out_print": 10,
    "test.framework.test.test_middleware.test_print.test_close_spider_print_05_cffex.Spider_Out_print": 10,
    # "test.framework.test.test_middleware.test_print.test_close_spider_csv_07_shfe.Spider_Out_CSV": 10,


    # 'test.framework.test.test_example.mutil_sold_info.close_spider_enable_sold.Enable_Child_Spider':10,
    # 'test.framework.test.test_example.mutil_sold_info.close_spider_db_sold.HouseInfoDB': 20


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
LOG_FORMATTER_CLASS = 'test.framework.log.log.LogFormat'
# 时间的格式
LOG_DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
LOG_DATE_FORMAT_SHORT = '%H:%M:%S'
# 写入文件的格式
LOG_FILE_FORMAT = '[%(levelname)s]-[%(asctime)s][%(threadName)s:%(thread)d]' \
                  '[task_id:%(name)s][%(filename)s:%(lineno)d]: %(message)s' # 其中name为getlogger指定的名字
LOG_FILE_FORMAT_01 = '[%(levelname)s][%(asctime)s]:%(message)s%(extra_info)s - [%(filename)s][line:%(lineno)d]\n '


# console输出的格式
LOG_NORMAL_FORMAT = '%(message)s-[%(levelname)s-%(asctime)s]'
LOG_DEBUG_SHORT_FORMAT = '%(message)s%(extra_info)s-[%(filename)s:%(lineno)d]'
LOG_DEBUG_LONG_FORMAT = '[%(levelname)s] [%(asctime)s]-[%(filename)s][line:%(lineno)d]: %(message)s%(extra_info)s'


LOG_ERROR_FORMAT = '[%(levelname)s] [%(asctime)s]-[%(filename)s][line:%(lineno)d]: %(message)s %(time)s'
LOG_ERROR_SHORT_FORMAT = '%(message)s %(time)s-[%(levelname)s-%(filename)s-line:%(lineno)d]'

# 记录爬取过程中出错的URL
LOG_FILE_ERROR_URL_FORMAT = '[%(asctime)s] [%(filename)s] [%(message)s] [%(reason)s] [%(exception)s][%(time)s]'


# MSG的格式
# crawled的格式
LOG_CRAWLED_MSG = 'Crawled:[%(module)s%(name)s%(function)s%(request)s] %(msg)s%(time)s'

# error的格式
LOG_ERROR_MSG = 'Error:[%(module)s%(name)s%(function)s%(request)s] %(msg)s%(exception)s'


LOG_FILE_PATH = 'C:\\Users\\scott\\PycharmProjects\\crawler\\log_record\\'
LOG_FILE_NAME  = LOG_FILE_PATH+'default_log_name.log'
LOG_FILE_ERROR_URL = 'default_error_url.log'
LOG_LEVEL = "DEBUG"


LOG_MONGODB_URL = "127.0.0.1:27017"
LOG_MONGODB_DATABASE = "LOG"
LOG_MONGODB_FORMAT = '[%(asctime)s] %(message)s'


LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file_format': {
            'format': LOG_FILE_FORMAT_01,
            'datefmt': LOG_DATE_FORMAT

        },
        'normal_format': {
            'format': LOG_NORMAL_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        },
        'debug_format': {
            'format': LOG_DEBUG_SHORT_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        },
        'error_format': {
            'format': LOG_ERROR_SHORT_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        },
        'error_url':{
            'format': LOG_FILE_ERROR_URL_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        },
        'db_format':{
            'format': LOG_MONGODB_FORMAT,
            'datefmt': LOG_DATE_FORMAT_SHORT
        }

    },
    'filters': {
        'error_filter':
            {
                '()':'test.framework.log.logfilter.ErrorFilter'
                }
    },
    'handlers': {
        #  打印到终端的日志
        'console_info': {
            'level': 'DEBUG',
            'class': 'test.framework.log.loghandler.ConsoleHandler',  # 自定义打印到屏幕
            'formatter': 'debug_format',
            'filter_error':True
            # 'filters': ['error_filter'],

        },
        'console_error': {
            'level': 'ERROR',
            'class': 'test.framework.log.loghandler.ConsoleErrorHandler',  # 自定义打印到屏幕
            'formatter': 'error_format',
        },
        # 打印到文件的日志,收集info及以上的日志
        # 'rollfile': {
        #     'level': 'DEBUG',
        #     'class': 'test.framework.log.loghandler.RotateFileHandler',  # 保存到文件
        #     'formatter': 'file_format',
        #     # 'filters': ['error_filter'],
        #     'filename': LOG_FILE_NAME,  # 日志文件
        #     'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
        #     'backupCount': 5,  # 当一个文件超过大小的时候，最多再添加5个文件
        #     'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        # },
        'onefile': {
            'level': 'DEBUG',
            'class': 'test.framework.log.loghandler.OnlyOneFileHandler',  # 保存到文件
            'formatter': 'file_format',
            # 'filters': ['error_filter'],
            'filename': LOG_FILE_NAME,  # 日志文件
            'mode': 'w',  # 文件的读写模式
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'ErrorUrl': {
            'level': 'ERROR',
            'class': 'test.framework.log.loghandler.RecordErrorUrl',  # 保存到文件
            'formatter': 'error_url',
            'filename': LOG_FILE_ERROR_URL,  # 日志文件
            'mode': 'w',  # 文件的读写模式
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'logtoMongdb':{
            'level': 'DEBUG',
            'class': 'test.framework.log.loghandler.LogToMongDB',  # 保存到文件
            'MongDB_URL':LOG_MONGODB_URL,
            'MongDB_DATABASE':LOG_MONGODB_DATABASE,
            # 'MongDB_Collection_Name':'test',
            # 'MONGODB_FORMAT':LOG_MONGODB_FORMAT,
            'formatter': 'db_format',

        }

    },
    'loggers': {
        #  logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['console_info'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': LOG_LEVEL,
            'propagate': True,  # 向上（更高level的logger）传递
        },

    },
}

#M
# MONGODB_URL = "149.28.192.96:27017"
MONGODB_URL = "127.0.0.1:27017"
MONGODB_NAME = "LianJia"
MONGODB_NAME_SOLD = 'PuDong_Sold'
#N
#O
#P
PROXY = [
    ("149.28.192.96",5527,'spider:123456'),
    ('47.105.165.81',5527,'spider:123456'),
]
#Q
#R
REACTOR_THREADPOOL_MAXSIZE = 10
RANDOMIZE_DOWNLOAD_DELAY = True  # 随机延迟
#S
SPIDER_MANAGER_CLASS = "test.framework.objectimport.spiderloader.SpiderLoader"
SCHEDULER = "test.framework.core.scheduler.Scheduler"
SPIDER_MIDDLEWARES = {
    # "test.framework.spider.spidermw.record_errurl.RecordSpiderErrorUrl": 10,
}
SPIDER_CHILD_CLASS = 'test.framework.test.test_spider.simple_spider.simple_spider_05_xiaoqu_house.SimpleSpider'
#T

#U
#V
#W
#X
#Y
#Z





