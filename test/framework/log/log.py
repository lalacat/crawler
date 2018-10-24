"""
logging配置
"""
import os
import logging.config
import warnings

from test.framework.log.test_logger_A import Log_A
# 定义三种日志输出格式 开始
from test.framework.setting import Setting


class LogFormat(object):
    # log配置字典

    def __init__(self,settings=None):
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
        self.settings =settings

    @classmethod
    def from_crawler(cls,crawler):
        return (crawler.settings)
    def _crawled(self,spider_name='spider',msg='Nothing',request=None):
        if not request:
            return {
                'msg': self.settings['LOG_CRAWLED_MSG'],
                'args': {
                    'spider_name':spider_name,
                    'msg':msg
                }
            }
        else:
            return {
                'msg': self.settings['LOG_CRAWLED_MSG'],
                'args': {
                    'spider_name':spider_name,
                    'request':request,
                    'msg':msg
                }
            }

    def crawled(self,spider_name='spider',msg='Nothing',request=None):
        return self.logformatter_adapter(self._crawled(spider_name,msg,request))

    def logformatter_adapter(self,logkws):
        """
        Helper that takes the dictionary output from the methods in LogFormatter
        and adapts it into a tuple of positional arguments for logger.log calls,
        handling backward compatibility as well.
        """
        if not {'msg', 'args'} <= set(logkws):
            warnings.warn("缺少必要的参数<msg><args>")

        message = logkws.get('msg')

        #  如果logkws含有'args'，则取 logkws['args']，负责直接为logkws本身
        args = logkws if not logkws.get('args') else logkws['args']

        return (message, args)

    def load_format(self):
        logging.config.dictConfig(self.settings['LOGGING_DIC'])  # 导入上面定义的logging配置

s = Setting()

a = LogFormat(s)
a.load_format()

logger = logging.getLogger(__name__)  # 生成一个log实例
logger.info('It works!')  # 记录该文件的运行状态
logger.info(*a.crawled("test",'works'))
