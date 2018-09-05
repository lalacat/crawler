from twisted.internet.defer import Deferred,succeed
from twisted.python.failure import Failure
from twisted.internet import reactor,defer

def got_poem(res,num):
    print("Your poem is served:",res)
    return "got it: "+str(num)

def test_fun_01(result):
    print("test_fun_01 ",result)
    return result

def test_fun_02(result):
    print("test_fun_02 ",result)
    return result

def test_fun_03(result):
    print("test_fun_03 ",result)
    return result

def test_fun_04(result):
    print("test_fun_04 ",result)
    return result


def poem_finish(result):
    print("finish :",result)


def poem_failed(err):
    print("No poetry for you")

def poem_done(_):
    from twisted.internet import reactor
    reactor.stop()

fun_list = [test_fun_01,test_fun_02,test_fun_03,test_fun_04]
#dfds = [defer.succeed("test").addCallback(x) for x in fun_list]



n = 0
dl = []
for i in fun_list:
    d = Deferred()
    d.addCallback(i)
    d.callback("test"+str(n))
    n += 1
    dl.append(d)
m = 0
for i in dl:
    i.addCallback(got_poem,m)
    m += 1

dd = defer.DeferredList(dl)


f = lambda r:[x for x in r]
#dd.addCallback(f)
dd.addCallback(poem_finish)
r = [(0,1),(1,2),(2,5),(3,6)]
'''



d = Deferred()
def cancel_delayed_call(result):
    if d1.active():
        print("cancel")
        d.cancel()
    return result
#d1.callback("no")
d.addCallback(cancel_delayed_call)
d1 = reactor.callLater(1,d.callback,"Another short poem")

d.addCallback(got_poem)

reactor.run()

print("Finish")'''
