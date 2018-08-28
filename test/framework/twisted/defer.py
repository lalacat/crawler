from twisted.internet import defer


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