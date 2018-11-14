import logging
from logging.handlers import RotatingFileHandler
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

class FileHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super(RotatingFileHandler, self).__init__(filename=self.filename, mode='a', maxBytes=self.maxBytes,
                                                  backupCount=self.backupCount, encoding=self.encoding, delay=False)

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

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if not hasattr(record, 'extra_info'):
            record.__dict__['extra_info'] = ' '
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0