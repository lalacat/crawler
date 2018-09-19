from pydispatch import dispatcher
from pydispatch.dispatcher import Any, Anonymous, liveReceivers, \
    getAllReceivers, disconnect
import logging
from twisted.internet.defer import maybeDeferred, DeferredList, Deferred
from twisted.python.failure import Failure

from pydispatch.robustapply import robustApply

logger = logging.getLogger(__name__)


class _IgnoredException(Exception):
    pass


class SignalManager(object):
    """处理信号相关的"""

    def __init__(self,sender = dispatcher.Anonymous):
        """Anonymous相当于信号发送对象为None"""

    def connect(self,receiver,signal,**kwargs):
        """
        用于将一个信号连接到接收对象
        :param receiver: 信号接收对象
        :param signal: 信号源
        :param kwargs:
        :return:
        """
        """为信号的发送对象指定一个默认对象"""
        kwargs.setdefault("sender",self.sender)
        return dispatcher.connect(receiver,signal,**kwargs)

    def disconnect(self,receiver,signal,**kwargs):
        """ 将一个信号与绑定的接受者解除连接"""

        kwargs.setdefault('sender', self.sender)
        return dispatcher.disconnect(receiver, signal, **kwargs)

    def send_catch_log(self,signal,**kwargs):
        """发送一个信号，捕捉Exception或者log"""
        kwargs.setdefault('sender', self.sender)
        return send_catch_log(signal, **kwargs)


def send_catch_log(signal=Any, sender=Anonymous, *arguments, **named):
    """Like pydispatcher.robust.sendRobust but it also logs errors and returns
    Failures instead of exceptions.
    """
    dont_log = named.pop('dont_log', _IgnoredException)
    spider = named.get('spider', None)
    responses = []
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        try:
            response = robustApply(receiver, signal=signal, sender=sender,
                *arguments, **named)
            if isinstance(response, Deferred):
                logger.error("Cannot return deferreds from signal handler: %(receiver)s",
                             {'receiver': receiver}, extra={'spider': spider})
        except dont_log:
            result = Failure()
        except Exception:
            result = Failure()
            logger.error("Error caught on signal handler: %(receiver)s",
                         {'receiver': receiver},
                         exc_info=True, extra={'spider': spider})
        else:
            result = response
        responses.append((receiver, result))
    return responses


def send_catch_log_deferred(signal=Any, sender=Anonymous, *arguments, **named):
    """Like send_catch_log but supports returning deferreds on signal handlers.
    Returns a deferred that gets fired once all signal handlers deferreds were
    fired.
    """
    def logerror(failure, recv):
        if dont_log is None or not isinstance(failure.value, dont_log):
            logger.error("Error caught on signal handler: %(receiver)s",
                         {'receiver': recv},
                         exc_info=failure_to_exc_info(failure),
                         extra={'spider': spider})
        return failure

    dont_log = named.pop('dont_log', None)
    spider = named.get('spider', None)
    dfds = []
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        d = maybeDeferred(robustApply, receiver, signal=signal, sender=sender,
                *arguments, **named)
        d.addErrback(logerror, receiver)
        d.addBoth(lambda result: (receiver, result))
        dfds.append(d)
    d = DeferredList(dfds)
    d.addCallback(lambda out: [x[1] for x in out])
    return d


def disconnect_all(signal=Any, sender=Any):
    """Disconnect all signal handlers. Useful for cleaning up after running
    tests
    """
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        disconnect(receiver, signal=signal, sender=sender)

def failure_to_exc_info(failure):
    """Extract exc_info from Failure instances"""
    if isinstance(failure, Failure):
        return (failure.type, failure.value, failure.getTracebackObject())