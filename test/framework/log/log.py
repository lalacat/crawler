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
        self._load_format()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def crawled(self, module, name, msg, extra=None):
        return self.logformatter_adapter(self._crawled(module, name, msg, extra))

    def error(self, module, name,function, msg):
        return self.logformatter_adapter(self._error(module, name,function, msg))


    def crawled_time(self,module,name,msg,time,extra=None):
        return self.logformatter_adapter(self._crawled_time(module, name, msg,time, extra))

    def _crawled(self,module,name,msg,extra=None):
        if not extra:
            return {
                'msg': self.settings['LOG_CRAWLED_MSG'],
                'args': {
                    'module':module,
                    'name':name,
                    'msg':msg
                }
            }
        elif isinstance(extra,dict):
            if isinstance(extra,dict):
                return {
                    'msg': self.settings['LOG_CRAWLED_REQUEST_EXTRA'],
                    'args': {
                        'module': module,
                        'name': name,
                        'function': extra['function'],
                        'request': extra['request'],
                        'msg': msg,
                    }
                }
        else:
            return {
                'msg': self.settings['LOG_CRAWLED_EXTRA'],
                'args': {
                    'module': module,
                    'name':name,
                    'extra_model':extra,
                    'msg':msg
                }
            }

    def _crawled_time(self,module,name,msg,time,extra=None):
        if not extra:
            return {
                'msg': self.settings['LOG_CRAWLED_TIME'],
                'args': {
                    'module':module,
                    'name':name,
                    'msg':msg,
                    'time':time
                }
            }
        elif isinstance(extra,dict):
            return {
                'msg': self.settings['LOG_CRAWLED_TIME_REQUEST_EXTRA'],
                'args': {
                    'module': module,
                    'name': name,
                    'msg': msg,
                    'function': extra['function'],
                    'request': extra['request'],
                    'time':time

                }
            }
        else:
            return {
                'msg': self.settings['LOG_CRAWLED_TIME_EXTRA'],
                'args': {
                    'module': module,
                    'name':name,
                    'extra_model':extra,
                    'msg':msg,
                    'time':time

                }
            }

    def _error(self,module, name, function,msg):
        error_msg = msg if msg else ''
        error_fun = function if function else ''
        if isinstance(error_fun,str) :
            return {
                'msg': self.settings['LOG_ERROR_MSG'],
                'args': {
                    'module': module,
                    'name': name,
                    'msg': error_msg,
                    'function': error_fun
                }
            }
        elif isinstance(error_fun,dict):
            return {
                'msg': self.settings['LOG_ERROR_REQUEST_EXTRA'],
                'args': {
                    'module': module,
                    'name': name,
                    'msg': error_msg,
                    'function': error_fun['function'],
                    'request' : error_fun['request']
                }
            }
        else:
            raise AttributeError("log输出参数错误")



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

    def _load_format(self):
        logging.config.dictConfig(self.settings['LOGGING_DIC'])  # 导入上面定义的logging配置



