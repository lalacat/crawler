class Countdown(object):

    counter = 5

    def count(self):
        if self.counter == 0 :
            reactor.stop()
        else:
            print(self.counter,'...')
            self.counter -= 1
            #callLater(time,call_fun)将来的几秒执行回调函数
            reactor.callLater(1,self.count)


from twisted.internet import reactor

reactor.callWhenRunning(Countdown().count)

print('start')
reactor.run()
print('stop')