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
        for i in range(5):
            self.slot.active.add(request)
        deferred = defer.Deferred().addBoth(_delactivate)
        self.slot.queue.append((request, deferred))
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

        while slot.queue and slot.free_transfer_slots() > 0:
            slot.lastseen = now
            print('lastseen:%6.3f'%slot.lastseen)
            if delay:
                self._process_queue(slot)
                break
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request)
            dfd.chainDeferred(deferred)



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

        print('download time :%6.3f'%time.clock())
        def test():
            print(request+':%6.3f' %time.clock())
            return 'Finish'

        return task.deferLater(reactor, 1,test)


def finish_print(_):
    print(_)
    reactor.stop()
test_download = Test_Download()

d = test_download._enqueue_request('test')

d.addBoth(finish_print)
reactor.run()
