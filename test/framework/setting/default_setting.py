TEST1 = "test1"
TEST2 = "test2"
LOG_FORMATTER = "AAA"
#A
#B

#C
CONCURRENT_REQUESTS = 16  # 设置的并发数
CONCURRENT_REQUESTS_PER_IP = 0  # ip并发度:
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # 设置HTTPConnectionPool最大保持连接个数

#D
DOWNLOADER = "test.framework.downloads.Downloader"
# 默认下载器
DOWNLOAD_HANDLER = "test.framework.downloads.download_agent.HTTPDownloadHandler"
DOWNLOAD_TIMEOUT = 180      # 3mins

#DOWNLOAD_MAXSIZE = 1024  # 1024m 下载网页大小的最大值
DOWNLOAD_MAXSIZE = 1024*1024*1024   # 1024m 下载网页大小的最大值
#DOWNLOAD_WARNSIZE = 32    # 32m 下载网页大小的警戒线
DOWNLOAD_WARNSIZE = 32*1024*1024    # 32m 下载网页大小的警戒值

DOWNLOAD_FAIL_ON_DATALOSS = True



#E
#F
#G
#H
#I
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





