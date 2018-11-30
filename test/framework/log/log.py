"""
logging配置
"""
import os
import logging.config
import pprint
import time
import warnings

from test.framework.log.test_logger_A import Log_A
# 定义三种日志输出格式 开始
from test.framework.setting import Setting
logger = logging.getLogger(__name__)





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
        self.level = settings['LOG_LEVEL']
        self.file_name = self._get_filename()
        self._update_loggingdict()
        self._load_format()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)

    def crawled(self, module, name, msg, extra=None):
        return self._logformatter_adapter(self._crawled(module, name, msg, extra))

    def error(self, module, name,function, msg):
        return self._logformatter_adapter(self._error(module, name,function, msg))

    def crawled_time(self,module,name,msg,time,extra=None):
        return self._logformatter_adapter(self._crawled_time(module, name, msg,time, extra))

    def _crawled(self,module,name,msg,extra=None):
        module_name = name if name is '' else ':'+str(name)
        if not extra:
            return {
                'msg': self.settings['LOG_CRAWLED_MSG'],
                'args': {
                    'module':module,
                    'name':module_name,
                    'msg':msg
                }
            }
        elif isinstance(extra,dict):
            if isinstance(extra,dict):
                return {
                    'msg': self.settings['LOG_CRAWLED_REQUEST_EXTRA'],
                    'args': {
                        'module': module,
                        'name': module_name,
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
                    'name':module_name,
                    'extra_model':extra,
                    'msg':msg
                }
            }

    def _crawled_time(self,module,name,msg,time,extra=None):
        module_name = name if name is '' else ':'+str(name)
        if not extra:
            return {
                'msg': self.settings['LOG_CRAWLED_TIME'],
                'args': {
                    'module':module,
                    'name':module_name,
                    'msg':msg,
                    'time':time
                }
            }
        elif isinstance(extra,dict):
            return {
                'msg': self.settings['LOG_CRAWLED_TIME_REQUEST_EXTRA'],
                'args': {
                    'module': module,
                    'name': module_name,
                    'msg': msg,
                    'time':time,
                    'function': extra['function'],
                    'request': extra['request'],

                }
            }
        else:
            return {
                'msg': self.settings['LOG_CRAWLED_TIME_EXTRA'],
                'args': {
                    'module': module,
                    'name':module_name,
                    'extra_model':extra,
                    'msg':msg,
                    'time':time

                }
            }

    def _error(self,module, name, function,msg):
        module_name = name if name is '' else ':'+str(name)
        error_msg = msg if msg else ''
        error_fun = function if function else ''
        if isinstance(error_fun,str) :
            return {
                'msg': self.settings['LOG_ERROR_MSG'],
                'args': {
                    'module': module,
                    'name': module_name,
                    'msg': error_msg,
                    'function': error_fun
                }
            }
        elif isinstance(error_fun,dict):
            return {
                'msg': self.settings['LOG_ERROR_REQUEST_EXTRA'],
                'args': {
                    'module': module,
                    'name': module_name,
                    'msg': error_msg,
                    'function': error_fun['function'],
                    'request' : error_fun['request']
                }
            }
        else:
            raise AttributeError("log输出参数错误")

    def _update_loggingdict(self):
        for name, logset in self.settings['LOGGING_DIC'].items():
            if name is 'handlers':
                if isinstance(logset, dict):
                    for key,value in logset.items():
                        if value.get('filename'):
                            value['filename'] = self.file_name

    def _get_filename(self):
        time_now = time.localtime(time.time())
        time_str = time.strftime('%Y%m%d', time_now)+'.log'
        root_path = os.getcwd()
        root_num = root_path.index('crawler')
        logfile_dir = os.path.join(root_path[:root_num+len('crawler')],'log_record')
        if not os.path.isdir(logfile_dir):
            os.makedirs(logfile_dir)
        file_name = os.path.join(logfile_dir,time_str)
        return file_name

    def _logformatter_adapter(self,logkws):
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
        # 导入上面定义的logging配置
        logging.config.dictConfig(self.settings['LOGGING_DIC'])


# root_path = os.getcwd()
# root = root_path.index('crawler')
#
# print(root)
# print(root_path[:root+len('crawler')])
# print(os.path.dirname(root_path[:root+len('crawler')]))

