import re

from twisted.internet import defer
from twisted.internet.endpoints import TCP4ClientEndpoint

from test.framework.https.parse_url import to_bytes


class TunnelingTCP4ClientEndpoint(TCP4ClientEndpoint):
    """An endpoint that tunnels through proxies to allow HTTPS downloads. To
    accomplish that, this endpoint sends an HTTP CONNECT to the proxy.
    The HTTP CONNECT is always sent when using this endpoint, I think this could
    be improved as the CONNECT will be redundant if the connection associated
    with this endpoint comes from the pool and a CONNECT has already been issued
    for it.
    """

    _responseMatcher = re.compile(b'HTTP/1\.. (?P<status>\d{3})(?P<reason>.{,32})')

    def __init__(self, reactor, host, port, proxyConf, contextFactory,
                 timeout=30, bindAddress=None):
        proxyHost, proxyPort, self._proxyAuthHeader = proxyConf
        super(TunnelingTCP4ClientEndpoint, self).__init__(reactor, proxyHost,
            proxyPort, timeout, bindAddress)
        self._tunnelReadyDeferred = defer.Deferred()
        self._tunneledHost = host
        self._tunneledPort = port
        self._contextFactory = contextFactory
        self._connectBuffer = bytearray()

    def requestTunnel(self, protocol):
        """Asks the proxy to open a tunnel."""
        tunnelReq = tunnel_request_data(self._tunneledHost, self._tunneledPort,
                                        self._proxyAuthHeader)
        protocol.transport.write(tunnelReq)
        self._protocolDataReceived = protocol.dataReceived
        protocol.dataReceived = self.processProxyResponse
        self._protocol = protocol
        return protocol

    def processProxyResponse(self, rcvd_bytes):
        """Processes the response from the proxy. If the tunnel is successfully
        created, notifies the client that we are ready to send requests. If not
        raises a TunnelError.
        """
        self._connectBuffer += rcvd_bytes
        # make sure that enough (all) bytes are consumed
        # and that we've got all HTTP headers (ending with a blank line)
        # from the proxy so that we don't send those bytes to the TLS layer
        #
        # see https://github.com/scrapy/scrapy/issues/2491
        if b'\r\n\r\n' not in self._connectBuffer:
            return
        self._protocol.dataReceived = self._protocolDataReceived
        respm = TunnelingTCP4ClientEndpoint._responseMatcher.match(self._connectBuffer)
        if respm and int(respm.group('status')) == 200:
            try:
                # this sets proper Server Name Indication extension
                # but is only available for Twisted>=14.0
                sslOptions = self._contextFactory.creatorForNetloc(
                    self._tunneledHost, self._tunneledPort)
            except AttributeError:
                # fall back to non-SNI SSL context factory
                sslOptions = self._contextFactory
            self._protocol.transport.startTLS(sslOptions,
                                              self._protocolFactory)
            self._tunnelReadyDeferred.callback(self._protocol)
        else:
            if respm:
                extra = {'status': int(respm.group('status')),
                         'reason': respm.group('reason').strip()}
            else:
                extra = rcvd_bytes[:32]
            self._tunnelReadyDeferred.errback(
                Exception('Could not open CONNECT tunnel with proxy %s:%s [%r]' % (
                    self._host, self._port, extra)))

    def connectFailed(self, reason):
        """Propagates the errback to the appropriate deferred."""
        self._tunnelReadyDeferred.errback(reason)

    def connect(self, protocolFactory):
        self._protocolFactory = protocolFactory
        connectDeferred = super(TunnelingTCP4ClientEndpoint,
                                self).connect(protocolFactory)
        connectDeferred.addCallback(self.requestTunnel)
        connectDeferred.addErrback(self.connectFailed)
        return self._tunnelReadyDeferred

def tunnel_request_data(host, port, proxy_auth_header=None):
    r"""
    Return binary content of a CONNECT request.

    """
    host_value = to_bytes(host, encoding='ascii') + b':' + to_bytes(str(port))
    tunnel_req = b'CONNECT ' + host_value + b' HTTP/1.1\r\n'
    tunnel_req += b'Host: ' + host_value + b'\r\n'
    if proxy_auth_header:
        tunnel_req += b'Proxy-Authorization: ' + proxy_auth_header + b'\r\n'
    tunnel_req += b'\r\n'
    return tunnel_req