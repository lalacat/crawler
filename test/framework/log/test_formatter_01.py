import logging


logger = logging.getLogger(__name__)
CRAWLEDMSG = u"Crawled:(%(spider_name)s)(%(status)s) %(request_and_response)s%(request_flags)s %(response_flags)s"

simple_format = '[%(asctime)s][%(filename)s:%(lineno)d] - Crawled: [Spdier:%(spider_name)s] %(mess)s'

try:
    logger.log(logging.WARN,simple_format,{'spider_name':'Test','mess':"This is Test!!"})
except Exception as e :
    print(e)