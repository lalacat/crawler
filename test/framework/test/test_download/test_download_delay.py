import time
from collections import deque

from twisted.internet import defer, reactor, task


class Slot(object):
    def __init__(self):
        self.delay = 5
        self.lastseen = 0
        self.active = set()
        self.queue = deque()
        self.latercall = None
        self.concurrency = 3
        self.transferring = set()


    def free_transfer_slots(self):
        return self.concurrency - len(self.transferring)


class Test_Download(object):

    def __init__(self):
        self.delay = 5
        self.lastseen = 0
        self.active = set()
        self.queue = deque()
        self.latercall = None
        self.slot = Slot()

    def _enqueue_request(self, request):

        def _delactivate(response):
            self.slot.active.remove(request)
            return response


        self.slot.active.add(request)
        deferred = defer.Deferred().addBoth(_delactivate)
        self.slot.queue.append((request, deferred))
        print(len(self.slot.queue))
        self._process_queue(self.slot)

        return deferred

    def _process_queue(self, slot):
        if slot.latercall and slot.latercall.active(): # 如果一个latercall正在运行则直接返回
            return

        now = time.clock()
        print('now:%6.3f'%now)
        delay = self.delay

        if delay:
            penalty = delay + slot.lastseen - now

            if penalty > 0 :
                print('penalty:%6.3f'%penalty)
                slot.latercall = reactor.callLater(penalty,self._process_queue,slot)
                return

        while slot.queue and slot.free_transfer_slots() > 0:
            print('_process_queue : %d' %len(self.slot.queue))

            slot.lastseen = now
            print('lastseen:%6.3f'%slot.lastseen)
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request)
            dfd.chainDeferred(deferred)

            if delay:
                self._process_queue(slot)
                break


    def _download(self, slot, request):
        # logger.debug("Spider:%s <%s> 正在下载...",spider.name,request)

        try:
            dfd = self.download(request)
        except Exception:
            raise ValueError("can't find spider")

        slot.transferring.add(request)

        def finish_transferring(_):
            slot.transferring.remove(request)
            self._process_queue(slot)
            return _

        return dfd.addBoth(finish_transferring)

    def download(self,request):

        print('%s download time :%6.3f'%(request,time.clock()))
        def test():
            print(request+':%6.3f' %time.clock())
            return request+'_Finish'

        return task.deferLater(reactor, 1,test)


def finish_print(_):
    print(_)
    return None
test_download = Test_Download()

ll = list()
for i in range(5):
    url = 'test_'+str(i)
    d = test_download._enqueue_request(url)
    d.addCallback(finish_print)
    ll.append(d)
dd = defer.DeferredList(ll)
dd.addBoth(lambda _: reactor.stop())
reactor.run()
