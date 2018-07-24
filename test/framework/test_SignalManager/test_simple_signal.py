from pydispatch import dispatcher

from pydispatch import dispatcher
SIGNAL = 'my-first-signal'

first_sender = object()
def handle_event( sender ):
    """Simple event handler"""
    print ('Signal was sent by', sender)
dispatcher.connect( handle_event, signal=SIGNAL, sender=dispatcher.Any)


second_sender = {}
if __name__ == "__main__":
    dispatcher.send( signal=SIGNAL, sender=first_sender )
    dispatcher.send( signal=SIGNAL, sender=second_sender )