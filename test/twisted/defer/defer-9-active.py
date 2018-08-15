from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from twisted.internet import reactor

def got_poem(res):
    print("Your poem is served:")
    print(res)


def poem_failed(err):
    print("No poetry for you")

def poem_done(_):
    from twisted.internet import reactor
    reactor.stop()




#d.addCallbacks(got_poem,poem_failed)
#d.addBoth(poem_done)

#d.callback("This poem is short.")


#d.errback(Failure(Exception("I have failed")))
d = Deferred()
d1 = reactor.callLater(0,d.callback,"Another short poem")
def cancel_delayed_call(result):
    if d1.active():
        print("cancel")
        d1.cancel()
    return result
d1.callback("no")
d.addCallback(cancel_delayed_call)
d.addCallback(got_poem)

reactor.run()

print("Finish")