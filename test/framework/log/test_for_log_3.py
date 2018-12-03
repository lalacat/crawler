import logging
import pprint

from test.framework.log.log import LogFormat
from test.framework.setting import Setting
from test.framework.log.logfilter import ErrorFilter
s = Setting()
a = LogFormat(s)

logger = logging.getLogger("lala")  # 生成一个log实例

logger.debug(*a.crawled("Spider","lala",
                       '出现出现错误',
                       {'function':'Scraper','request':"baba"}),
            extra={'extra_info':'error'})


logger.info(*a.crawled_time("Spider",'works',
                            'info',
                            6.7777777,
                            "engine"),
            extra={
                "extra_info":" inprogress中还剩下{:d}个任务".format(3)})


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
                          '出现错误{name}'.format(name='lili')),
             extra=
             {
                 'exception':'info',
                'time':"\n时间是{:d}".format(34)
             })
logger.error(*a.error("Spider","lala",
                      {
                          'function':'Scraper',
                          'request':'www'
                      },
                          '出现错误{name}'.format(name='lili')),
             extra=
             {
                'reason':'finish',
                 'exception':'info',
                'time':"\n时间是{:d}".format(34)
             })
error_msg = ("%(url)s 网页的大小(%(size)s)已经超过可容许下载的最大值(%(maxsize)s).")
error_args = {'url': 'wwww', "size": 20, 'maxsize': 30}
# logger.error(error_msg, error_args)
logger.error(*a.error("Spider","lala",
                      {
                          'function':'Scraper',
                          'request':'www'
                      },
                          "{url} 网页的大小{size}已经超过可容许下载的最大值({maxsize}).".format(**error_args)),
             extra=
             {
                 'exception':'info',
                'time':"\n时间是{:d}".format(34)
             })

args = {'clsname': "lili", 'eargs': "bibi"}
pplist = ['q','w','e','r']
logger.warning(*a.crawled(
    "Middleware", 'pupu',
    '未生效:'),
               extra={
                   'extra_info': '{clsname}s: %{eargs}s'.format(**args)
               }

               )
logger.warning(*a.crawled(
    "Middleware", 'pupu',
    '生效:'),
               extra={
                   'extra_info': pprint.pformat(pplist)
               }

               )
# logger.info("添加或重写的设置如下：\n %s", pprint.pformat(args))


logger.warning(*a.crawled(
    "Middleware", 'pupu',
    '生效:',
    '处理后的结果类型是{0},下一步进行process_item并行处理'.format("gyhj"))
               )

logger.error(*a.error('Spider',"asdsa",'',
                             '收取到的信息容量({bytes}) bytes 超过了下载信息的最大值({maxsize}) bytes '.format(
                                 bytes= 20,
                                 maxsize=10)
                             ))
logger.error('www.baidu.com', extra={
    'exception': '重复下载次数已超过最大值，判断此网页没有数据',
    'time': 120,
    'reason': 'No Data'
})