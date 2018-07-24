import logging  # 引入logging模块

logger = logging.getLogger(__name__)
def fun(a):
    print(a)
    return "test fun"
extr_dict = {'username':"lala","age":12}

logger_self = logging.LoggerAdapter(logger,extr_dict)

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
logger_self.info('this is a loggging info message')
logger_self.debug('this is a loggging debug message')
logger_self.warning('this is loggging a warning message', exc_info=fun(2),extra={"a":1})
logger_self.error('this is an loggging error message')
logger_self.critical('this is a loggging critical message')




logging.log(logging.CRITICAL, "This is a info log.")
