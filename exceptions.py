class UsageError(Exception):
    def __init__(self,*a,**kw):
        self.print_help = kw.pop("print_help",True)
        super(UsageError,self).__init__(*a,**kw)

class TunnelError(Exception):
    """An HTTP CONNECT tunnel could not be established by the proxy."""