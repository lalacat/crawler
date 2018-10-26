import logging

from test.framework.log.log import LogFormat
from test.framework.setting import Setting

s = Setting()

a = LogFormat(s)

logger = logging.getLogger(__name__)  # 生成一个log实例
# logger.info('It works!',extra={'extra_info':"lala"})  # 记录该文件的运行状态
#
# logger.infoed(*a.crawled("test",'works','lala'),extra={"extra_info":"inprogress中还剩下{:d}个任务".format(3)})
# logger.info(a.crawled("test",'works',"lala","Engine")[0],{"test",'works',"lala","Engine"})
# logger.info(*a.crawled("test",'works',"lala","Engine"))
# logger.info(*a.crawled_time("test",'works',"lala",6.7777777))
# logger.info(*a.crawled_time("test",'works',"lala",6.7777777,"engine"),extra={"extra_info":"inprogress中还剩下{:d}个任务".format(3)})
#
# logger.info(*a.crawl("test",'works','lala',{'request':'www.baidu.com'}))  # 记录该文件的运行状态
# logger.info(*a.crawled("test",'works','lala',{'function':'haha','request':'www.baidu.com'}))  # 记录该文件的运行状态

logger.error(*a.crawled("Spider","lala",
                                       '出现出现错误',{'function':'Scraper','request':"baba"}),extra={'extra_info':'error'}
                                              )

