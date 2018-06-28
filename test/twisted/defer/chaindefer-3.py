
from twisted.internet.defer import Deferred ,returnValue ,inlineCallbacks ,DeferredList ,CancelledError
from twisted.internet import reactor
from twisted.web.client import getPage
import twisted.internet.defer
d1 = Deferred()
d2 = Deferred()
d1.chainDeferred(d2)
d2.callback('hey')
d1.callback('jude')