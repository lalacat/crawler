import logging

from test.framework.log.log import LogFormat
from test.framework.setting import Setting
from test.framework.log.logfilter import ErrorFilter
s = Setting()

a = LogFormat(s)

logger = logging.getLogger("lala")  # 生成一个log实例

logger.info(*a.crawled("Spider","lala",
                       '出现出现错误',
                       {'function':'Scraper','request':"baba"}),
            extra={'extra_info':'error'})


logger.info(*a.crawled_time("Spider",'works',
                            'info',
                            6.7777777,
                            "engine"),
            extra={
                "extra_info":"inprogress中还剩下{:d}个任务".format(3)})


logger.info(*a.crawled("Spider","lala",
                                    '出现出现错误',
                        {
                            'function':'Scraper',
                            'request':"baba"
                        }),
             extra={'extra_info':'error'})
logger.error(*a.error("Spider","lala",
                      {
                          'function':'Scraper',
                          'request':'www'
                      },
                          '出现错误',),
             extra=
             {
                 'exception':'info',
                'time':"\n时间是{:d}".format(34)
             })

