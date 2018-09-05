from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

def got_poem(res):
    print("Your poem is served:")
    print(res)


def poem_failed(err):
    print("No poetry for you")

def poem_done(_):
    from twisted.internet import reactor
    reactor.stop()


d = Deferred()

d.addCallbacks(got_poem,poem_failed)
d.addBoth(poem_done)

#d.callback("This poem is short.")


#d.errback(Failure(Exception("I have failed")))

from twisted.internet import reactor
reactor.callWhenRunning(d.callback,"Another short poem")
reactor.run()

print("Finish")