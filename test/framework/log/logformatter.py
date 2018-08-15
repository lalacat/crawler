import os
import logging
from twisted.python.failure import Failure


"""
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

"""
SCRAPEDMSG = u"Scraped from %(src)s" + os.linesep + "%(item)s"# os.linesep代表回车
DROPPEDMSG = u"Dropped: %(exception)s" + os.linesep + "%(item)s"
CRAWLEDMSG = u"Crawled:(%(spider_name)s)(%(status)s) %(request_and_response)s%(request_flags)s %(response_flags)s"

class LogFormatter(object):
    """
    为不同的动作生成对应的log格式。

    方法输出字典的关键字有：
    - 'level':log的输出等级logging.DEBUG, logging.INFO,
        logging.WARNING, logging.ERROR and logging.CRITICAL
    - 'msg'代表的是不同动作的formatter格式
    - 'args'是msg的格式中对应的关键字，类型必须是dict或者是tuple
    """
    def crawled(self,request,response,spider):
        request_flags = ' %s' % str(request.flags) if request.flags else ''
        response_flags = ' %s' % str(response.flags) if response.flags else ''
        return {
            'level': logging.DEBUG,
            'msg': CRAWLEDMSG,
            'args': {
                'spider_name': spider.name,
                'status': response.status,
                'request_and_response': request,
                'request_flags': request_flags,
                #'referer': referer_str(request_and_response),
                'response_flags': response_flags,
                # backward compatibility with Scrapy logformatter below 1.4 version
                'flags': response_flags
            }
        }

    def scraped(self, item, response, spider):
        if isinstance(response, Failure):
            src = response.getErrorMessage()
        else:
            src = response
        return {
            'level': logging.DEBUG,
            'msg': SCRAPEDMSG,
            'args': {
                'src': src,
                'item': item,
            }
        }

    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.WARNING,
            'msg': DROPPEDMSG,
            'args': {
                'exception': exception,
                'item': item,
            }
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
