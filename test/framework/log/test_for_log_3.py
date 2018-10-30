import logging

from test.framework.log.log import LogFormat
from test.framework.setting import Setting
from test.framework.log.logfilter import ErrorFilter
s = Setting()

a = LogFormat(s)

logger = logging.getLogger(__name__)  # 生成一个log实例
#logger.addFilter(f)
logger.debug(*a.crawled("Spider","lala", '出现出现错误',{'function':'Scraper','request':"baba"}),extra={'extra_info':'error'})
logger.info(*a.crawled("Spider","lala", '出现出现错误',{'function':'Scraper','request':"baba"}),extra={'extra_info':'info'})

