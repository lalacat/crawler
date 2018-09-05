# 添加系统事件触发事件eventType： 包括'startup', 'shutdown',和 'persist'，以及三个状态调节phase：'before', 'during'和 'after'
#这些时间能够在reactor中内部激活，
#只有这些事件能够在reactor中实现
#已经挂载上的callbacks在before条件下，返回的要么是None要么是Deferred；当Deferred在before条件下激活后，during条件就不能执行了
#当during条件被激活的时候，所有还没激活的事件触发都要被触发，他们的返回值都会被忽略
def addSystemEventTrigger(phase, eventType, callable, *args, **kw):
    pass
