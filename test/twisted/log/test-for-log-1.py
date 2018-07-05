import logging  # 引入logging模块

logger = logging.getLogger(__name__)
def fun(a):
    print(a)
    return "test fun"

#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
logger.info('this is a loggging info message')
logger.debug('this is a loggging debug message')
logger.warning('this is loggging a warning message', exc_info=fun(2),extra={"a":1})
logger.error('this is an loggging error message')
logger.critical('this is a loggging critical message')

logging.log(logging.CRITICAL, "This is a info log.")
