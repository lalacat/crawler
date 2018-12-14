import base64
import json
import re
from pprint import pformat

from lxml import etree
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import ClientContextFactory
from twisted.python.log import err
from twisted.web.client import ProxyAgent, readBody, RedirectAgent
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint, _WrappingFactory
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implementer

from test.framework.https.parse_url import to_bytes


def display(response):
    print(response)
class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self,hostname, port):
        return ClientContextFactory.getContext(self)


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
        r = json.loads(self.result)
        #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
        #body传输到下一个函数中去
        self.finished.callback(r)

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


contextFactory = WebClientContextFactory()




def cbRequest(response):
    print('Redirect Response code:', response.code)
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished


def redirect(response):

    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    # url = response.headers.getRawHeaders('Location')[0].encode('utf-8')
    #
    # d = agent.request(b'GET',url, Headers({'Proxy-Authorization': [encode_user]}))
    # d.addCallback(cbRequest)
    # d.addCallback(get_onePage)

    d = readBody(response)
    d.addCallback(get_onePage)


    return d

host_01 = "149.28.192.96"
host = '47.105.165.81'
port = 5527
# header = Headers()
user_name = base64.b64encode('spider:123456'.encode('utf-8')).strip()
encode_user = b'Basic '+user_name
endpoint = TCP4ClientEndpoint(reactor, host, port)

agent = ProxyAgent(endpoint)
d = agent.request(b"GET", b"http://www.zimuzu.tv/",  Headers({'Proxy-Authorization': [encode_user]}))
d.addCallback(redirect)
d.addErrback(display)
d.addCallback(lambda ignored: reactor.stop())
reactor.run()

