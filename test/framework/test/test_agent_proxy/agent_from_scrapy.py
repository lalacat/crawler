import base64
import json
import re

from OpenSSL import SSL
from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import Agent, URI
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implementer

from exceptions import TunnelError
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
                TunnelError('Could not open CONNECT tunnel with proxy %s:%s [%r]' % (
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

    #
    # >>> to_unicode(tunnel_request_data("example.com", 8080))
    # 'CONNECT example.com:8080 HTTP/1.1\r\nHost: example.com:8080\r\n\r\n'
    # >>> s(tunnel_request_data("example.com", 8080, b"123"))
    # 'CONNECT example.com:8080 HTTP/1.1\r\nHost: example.com:8080\r\nProxy-Authorization: 123\r\n\r\n'
    # >>> s(tunnel_request_data(b"example.com", "8090"))
    # 'CONNECT example.com:8090 HTTP/1.1\r\nHost: example.com:8090\r\n\r\n'
    """
    host_value = to_bytes(host, encoding='ascii') + b':' + to_bytes(str(port))
    tunnel_req = b'CONNECT ' + host_value + b' HTTP/1.1\r\n'
    tunnel_req += b'Host: ' + host_value + b'\r\n'
    if proxy_auth_header:
        tunnel_req += b'Proxy-Authorization: ' + proxy_auth_header + b'\r\n'
    tunnel_req += b'\r\n'
    return tunnel_req

class TunnelingAgent(Agent):
    """An agent that uses a L{TunnelingTCP4ClientEndpoint} to make HTTPS
    downloads. It may look strange that we have chosen to subclass Agent and not
    ProxyAgent but consider that after the tunnel is opened the proxy is
    transparent to the client; thus the agent should behave like there is no
    proxy involved.
    """

    def __init__(self, reactor, proxyConf, contextFactory=None,
                 connectTimeout=None, bindAddress=None, pool=None):
        super(TunnelingAgent, self).__init__(reactor, contextFactory,
            connectTimeout, bindAddress, pool)
        self._proxyConf = proxyConf
        self._contextFactory = contextFactory

    def _getEndpoint(self, uri):
        return TunnelingTCP4ClientEndpoint(
            self._reactor, uri.host, uri.port, self._proxyConf,
            self._contextFactory, self._endpointFactory._connectTimeout,
            self._endpointFactory._bindAddress)

    def _requestWithEndpoint(self, key, endpoint, method, parsedURI,
            headers, bodyProducer, requestPath):
        # proxy host and port are required for HTTP pool `key`
        # otherwise, same remote host connection request could reuse
        # a cached tunneled connection to a different proxy
        key = key + self._proxyConf
        return super(TunnelingAgent, self)._requestWithEndpoint(key, endpoint, method, parsedURI,
            headers, bodyProducer, requestPath)

class ScrapyProxyAgent(Agent):

    def __init__(self, reactor, proxyURI,
                 connectTimeout=None, bindAddress=None, pool=None):
        super(ScrapyProxyAgent, self).__init__(reactor,
                                               connectTimeout=connectTimeout,
                                               bindAddress=bindAddress,
                                               pool=pool)
        self._proxyURI = URI.fromBytes(proxyURI)

    def request(self, method, uri, headers=None, bodyProducer=None):
        """
        Issue a new request via the configured proxy.
        """
        # Cache *all* connections under the same key, since we are only
        # connecting to a single destination, the proxy:

        proxyEndpoint = self._getEndpoint(self._proxyURI)

        key = ("http-proxy", self._proxyURI.host, self._proxyURI.port)
        return self._requestWithEndpoint(key, proxyEndpoint, method,
                                         URI.fromBytes(uri), headers, bodyProducer, uri)





def get_onePage(response):
    print(response)
    one_page = list()

    seletor = etree.HTML(response)

    #  总小区数
    total_number_community = seletor.xpath("/html/body/div[4]/div[1]/div[2]/h2/span/text()")[0]

    # 所有小区列表
    all_communities = seletor.xpath('/html/body/div[4]/div[1]/ul/li')
    for community in all_communities:
        result = dict()
        # 小区总信息
        community_info = community.xpath('./div[@class="info"]')[0]

        # 小区名称
        community_name = community_info.xpath('./div[@class="title"]/a')[0].text
        result["community_name"] = community_name
        print(community_name)

        # 小区url
        community_url = community_info.xpath('./div[@class="title"]/a')[0].get('href')
        result["community_url"] = community_url
        print(community_url)

        # 小区房屋信息
        community_sale_num = community_info.xpath('./div[@class="houseInfo"]/a[1]')[0].text
        community_rent_num = community_info.xpath('./div[@class="houseInfo"]/a[2]')[0].text
        community_onsale_num = community_info.xpath('../div[@class="xiaoquListItemRight"]/div[2]/a/span/text()')[0]

        result["community_sale_num"] = re.findall('\d+',community_sale_num)[1]
        result["community_rent_num"] = re.findall('\d+',community_rent_num)[0]
        result["community_onsale_num"] = community_onsale_num

        print(community_sale_num,re.findall('\d+',community_sale_num)[1])
        print(community_rent_num,re.findall('\d+',community_rent_num)[0])
        print("正在出售的房屋有：%s"%community_onsale_num)
        # 小区年限
        community_bulid_year = community_info.xpath('./div[@class="positionInfo"]/text()')[3].replace('/',"").strip()
        if str(community_bulid_year) == '未知年建成':
            print(community_bulid_year)
        else:
            print(community_bulid_year,re.findall('\d+',community_bulid_year)[0])
        result["community_bulid_year"] = community_bulid_year


        # 小区均价/html/body/div[4]/div[1]/ul/li[1]/div[2]
        community_avr_price = community_info.xpath('../div[@class="xiaoquListItemRight"]/div/div/span/text()')[0]
        result["community_avr_price"] = community_avr_price

        print(community_avr_price)
        one_page.append(result)
        print("\n")
    return one_page

@implementer(IBodyProducer)
class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        #用来保存传输的数据，当数据完整后可以使用json转换为python对象
        self.result = bytes()

    def dataReceived(self, datas):
        '''
        直接传输的数据datas为bytes类型的，不加解码转化为str类型是带有转义符号'\':(\'\\u5929\\u732b\\u7cbe\\u9009\')
        datas进行了decode("utf-8")解码后，数据变成了('\u5929\u732b\u7cbe\u9009'),此时解码后的数据类型是str
        因为传输的datas并不是一次性传输完的，所以不能直接使用json转换，而是当数据全部传输完毕后，使用json.loads()
        这时候就不涉及到转码和转义字符的问题了。
        '''
        self.result += datas

    def connectionLost(self, reason):
        print('Finished receiving body:', reason)
        #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
        #body传输到下一个函数中去
        self.finished.callback(self.result)


def cbRequest(response):
    print('Redirect Response code:', response.code)
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished))
    finished.addCallback(get_onePage)
    return finished


user_name = base64.b64encode('spider:123456'.encode('utf-8')).strip()
encode_user = b'Basic '+user_name
header = {'Proxy-Authorization': [encode_user]}
proxy_config = ('47.105.165.81',5527,encode_user)


class ScrapyClientContextFactory(ClientContextFactory):
    "A SSL context factory which is more permissive against SSL bugs."

    # see https://github.com/scrapy/scrapy/issues/82
    # and https://github.com/scrapy/scrapy/issues/26
    # and https://github.com/scrapy/scrapy/issues/981

    def __init__(self, method=SSL.SSLv23_METHOD):
        self.method = method

    def getContext(self, hostname=None, port=None):
        ctx = ClientContextFactory.getContext(self)
        # Enable all workarounds to SSL bugs as documented by
        # https://www.openssl.org/docs/manmaster/man3/SSL_CTX_set_options.html
        ctx.set_options(SSL.OP_ALL)
        return ctx


contextFactory = ScrapyClientContextFactory()

agent = TunnelingAgent(reactor,proxy_config,contextFactory,10,None,None)

d = agent.request(b'GET',b'https://smzdm.com',None,None)
d.addCallback(cbRequest)
d.addErrback(lambda _:print(_))
d.addBoth(lambda _:reactor.stop())
reactor.run()