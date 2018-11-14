import logging
from logging.handlers import RotatingFileHandler
logging.FileHandler


class ConsoleHandler(logging.StreamHandler):

    def __init__(self, *args, **kwargs):
        super(ConsoleHandler, self).__init__(*args, **kwargs)

    # 每进行一次log就会调用这个方法
    def emit(self, record):
        if not hasattr(record, 'extra_info'):
            record.__dict__['extra_info'] = ' '
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


class ConsoleErrorHandler(logging.StreamHandler):

    def __init__(self, *args, **kwargs):
        super(ConsoleErrorHandler, self).__init__(*args, **kwargs)

    # 每进行一次log就会调用这个方法
    def emit(self, record):
        if not hasattr(record, 'time'):
            record.__dict__['time'] = ' '
        if not hasattr(record, 'exception'):
            record.__dict__['exception'] = ' '
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


class RotateFileHandler(RotatingFileHandler):
    #  不覆盖原有的文件，一直生成
    def __init__(self,filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        super(RotateFileHandler, self).__init__(filename=filename,mode=mode,
                                                  maxBytes=maxBytes,
                                                  backupCount=backupCount,
                                                  encoding=encoding,
                                                  delay=delay)

    # 每进行一次log就会调用这个方法
    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        if not hasattr(record, 'extra_info'):
            record.__dict__['extra_info'] = ' '
        try:
            if self.shouldRollover(record):
                self.doRollover()
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)


class OnlyOneFileHandler(logging.FileHandler):
    def __init__(self,filename, mode='a', encoding=None, delay=False):
        super(OnlyOneFileHandler, self).__init__(filename=filename,mode=mode,
                                                  encoding=encoding,
                                                  delay=delay)
    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        if not hasattr(record, 'extra_info'):
            record.__dict__['extra_info'] = ' '
        if self.stream is None:
            self.stream = self._open()
        logging.StreamHandler.emit(self, record)