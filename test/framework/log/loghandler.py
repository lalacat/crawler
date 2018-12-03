import json
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


class RecordErrorUrl(logging.FileHandler):
    def __init__(self,filename, mode='a', encoding=None, delay=False):
        super(RecordErrorUrl, self).__init__(filename=filename,mode=mode,
                                                  encoding=encoding,
                                                  delay=delay)

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        if not hasattr(record, 'reason'):
            return
        if self.stream is None:
            self.stream = self._open()
        try:
            msg = self._format(record)
            stream = self.stream
            json.dump(msg,stream,ensure_ascii=False)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)
        # logging.StreamHandler.emit(self, record)

    def _format(self,record):
        format_data = dict()
        if hasattr(record, 'asctime'):
            format_data['asctime'] = record.__dict__['asctime']
        if hasattr(record,'msg'):
            format_data['url'] = record.__dict__['msg']
        if hasattr(record,'filename'):
            format_data['filename'] = record.__dict__['filename']
        if hasattr(record,'reason'):
            format_data['reason'] = record.__dict__['reason']
        if hasattr(record,'exception'):
            format_data['exception'] = record.__dict__['exception']
        if hasattr(record,'time'):
            format_data['time'] = record.__dict__['time']
        return format_data

# d = json.loads("[ERROR] [12/04/2018 00:26:46 AM]-[test_for_log_3.py][line:54]: Error:[Spider:lala Scraper www] 出现错误lili  finish")
# print(d)