import logging
logger = logging.getLogger(__name__)
LOG_DEBUG_FORMAT = '[%(levelname)s] [%(asctime)s]-[%(filename)s][line:%(lineno)d]: %(message)s %(eee)s'

class StreamHandler_DIY(logging.StreamHandler):
    """Record log levels count into a crawler stats"""

    def __init__(self, *args, **kwargs):
        super(StreamHandler_DIY, self).__init__(*args, **kwargs)
        print(args)

    #每进行一次log.info就会调用这个方法，从而可以计算出调用多少次

    def emit(self, record):
        if hasattr(record,'eee'):
            print('true')
        else:
            record.__dict__['eee']  = "AAA"
        # print(record.__dict__)
        print()
        msg = self.format(record)
        print(msg)

if __name__ == "__main__":
    handler= StreamHandler_DIY()
    # handler= logging.StreamHandler()
    fomatter = logging.Formatter(LOG_DEBUG_FORMAT)
    handler.setFormatter(fomatter)
    logger.addHandler(handler)
    logger.setLevel(level=logging.INFO)

    logger.info('this is 1 loggging info message',extra={'eee':"ddd"})
    # logger.info('this is 2 loggging info message')
    logger.info('this is 3 loggging info message')

