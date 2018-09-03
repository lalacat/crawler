from twisted.internet import defer,reactor
import logging

from twisted.python import failure

logger = logging.getLogger(__name__)


def defer_fail(_failure):
    """Same as twisted.internet.defer.fail but delay calling errback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go through readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    d = defer.Deferred()
    reactor.callLater(0.1, d.errback, _failure)
    return d

def defer_succeed(result):
    """Same as twisted.internet.defer.succeed but delay calling callback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go trough readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    d = defer.Deferred()
    reactor.callLater(0.1, d.callback, result)
    return d

def defer_result(result):
    if isinstance(result, defer.Deferred):
        return result
    elif isinstance(result, failure.Failure):
        return defer_fail(result)
    else:
        return defer_succeed(result)


def mustbe_deferred(f, *args, **kw):
    """Same as twisted.internet.defer.maybeDeferred, but delay calling
    callback/errback to next reactor loop
    """
    logging.info("进行mustbe_defferred包装")
    try:
        logging.info(f)
        logging.info(args)
        result = f(*args, **kw)

    # FIXME: Hack to avoid introspecting tracebacks. This to speed up
    # processing of IgnoreRequest errors which are, by far, the most common
    # exception in Scrapy - see #125
    except Exception as e:
        return defer_fail(failure.Failure(e))
    except:
        return defer_fail(failure.Failure())
    else:
        return defer_result(result)


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