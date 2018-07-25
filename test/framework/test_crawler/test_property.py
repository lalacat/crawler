
class A(object):
    crawlers = property(
        lambda self: self._crawlers,
        doc="Set of :class:`crawlers <scrapy.crawler.Crawler>` started by "
            ":meth:`crawl` and managed by this class."
    )

    def __init__(self,l):
        self._crawlers = l

l = list()
for i in range(10):
    l.append(i)

a = A(l)
print(A.crawlers.__doc__)