from twisted.internet import defer
import logging

from twisted.python import failure

logger = logging.getLogger(__name__)


def process_parallel(callbacks, input, *a, **kw):
    """
    并行处理
    返回一个Deferred，它的result是一个list，list里的内容是所有callbacks方法执行后的结果
    1.succeed的作用是返回一个Deferred,并直接执行了callback(input)，
    相当于返回一个带有result的Deferred,可以等价于执行：
    dfds = []
    for i in callbacks:
        d = Deferred()
        d.addCallback(i)
        d.callback(input)
        n += 1
        dfds.append(d)
    2.并行处理的目的是为了同时得到所有callbacks的执行结果，DeferredList执行后返回的结果就是一个list分别对应相应的Deferred,
    而每个result都是一个truple类型，(True, result),因此通过lambda函数处理，构造一个只有result的列表
    """
    dfds = [defer.succeed(input).addCallback(x, *a, **kw) for x in callbacks]
    d = defer.DeferredList(dfds, fireOnOneErrback=1, consumeErrors=1)
    d.addCallbacks(lambda r: [x[1] for x in r], lambda f: f.value.subFailure)
    return d


def process_chain(callbacks, input, *a, **kw):
    """
    返回一条串行处理的方法链，真对数据需要不同函数依次处理，最后返回一个带着处理后的result的Deferred
    :param callbacks: 回调函数
    :param input: defer之间传输的result
    :return: Deferred
    """
    d = defer.Deferred()
    for x in callbacks:
        d.addCallback(x, *a, **kw)
    d.callback(input)
    return d

def process_chain_both(callbacks,errbacks,input,*a,**kw):
    d = defer.Deferred()
    for cb,eb in zip(callbacks,errbacks):
        d.addCallbacks(cb,eb,callbackArgs=a,callbackKeywords=kw,
                       errbackArgs=a,errbackKeywords=kw)
    if isinstance(input,failure.Failure):
        d.errback(input)
    else:
        d.callback(input)
    return d