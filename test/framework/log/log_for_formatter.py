"""
logging配置
"""

import os
import logging.config
from test.framework.log.test_logger_A import Log_A
# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s]: %(message)s' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]: %(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"


# 定义日志输出格式 结束
'''
logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录

logfile_name = 'all2.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)
'''
# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format,
            'datefmt': DATE_FORMAT

        },
        'simple': {
            'format': simple_format,
            'datefmt':DATE_FORMAT
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple',
        },
        #打印到文件的日志,收集info及以上的日志

        #'default': {
        #    'level': 'DEBUG',
            #'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
        #    'formatter': 'standard',
            #'filename': logfile_path,  # 日志文件
        #    'maxBytes': 1024*1024*5,  # 日志大小 5M
        #    'backupCount': 5,
        #    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        #},

    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

CRAWLEDMSG = 'Crawled: [Spdier:%(spider_name)s] %(msg)s'
def crawled(name):
    return {
        'level': logging.DEBUG,
        'msg': CRAWLEDMSG,
        'args': {
            'spider_name':name,
            'msg':'successful'
        }
    }
def logformatter_adapter(logkws):
    """
    Helper that takes the dictionary output from the methods in LogFormatter
    and adapts it into a tuple of positional arguments for logger.log calls,
    handling backward compatibility as well.
    """
    if not {'level', 'msg', 'args'} <= set(logkws):
        #  warnings.warn('Missing keys in LogFormatter method',ScrapyDeprecationWarning)
        pass
    if 'format' in logkws:
        #warnings.warn('`format` key in LogFormatter methods has been ''deprecated, use `msg` instead',ScrapyDeprecationWarning)
        pass
    level = logkws.get('level', logging.INFO)
    message = logkws.get('format', logkws.get('msg'))

    #  如果logkws含有'args'，则取 logkws['args']，负责直接为logkws本身
    args = logkws if not logkws.get('args') else logkws['args']

    return (message, args)


logkws = {'a':"A",'b':"B",'c':"C"}
args = logkws if not logkws.get('args') else logkws['a']
print(args)


logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
logger = logging.getLogger(__name__)  # 生成一个log实例
logger.info('It works!')  # 记录该文件的运行状态
logger.info(CRAWLEDMSG,{'spider_name':'Test','msg':"successful"})
logger.info(*logformatter_adapter(crawled("test")))
A = Log_A()
