import base64
import json
import re
import time
from io import BytesIO
from pprint import pformat

from OpenSSL import SSL
from lxml import etree
from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Protocol
from twisted.internet.ssl import ClientContextFactory
from twisted.web.client import Agent, URI, RedirectAgent, ProxyAgent
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implementer

from test.framework.downloads.contextfactory import ScrapyClientContextFactory
from test.framework.downloads.proxy_agent import TunnelingAgent
from test.framework.https.parse_url import _parsed


def get_onePage(response):
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
        self._bodybuf = BytesIO()  # 记录body的内容

    def dataReceived(self, data):
        '''
        直接传输的数据datas为bytes类型的，不加解码转化为str类型是带有转义符号'\':(\'\\u5929\\u732b\\u7cbe\\u9009\')
        datas进行了decode("utf-8")解码后，数据变成了('\u5929\u732b\u7cbe\u9009'),此时解码后的数据类型是str
        因为传输的datas并不是一次性传输完的，所以不能直接使用json转换，而是当数据全部传输完毕后，使用json.loads()
        这时候就不涉及到转码和转义字符的问题了。
        '''
        self._bodybuf.write(data)

    def connectionLost(self, reason):
        print('Finished receiving body:', reason)
        try:
            body = self._bodybuf.getvalue()
            #callback(data)调用后，能够向defer数据链中传入一个list数据：[True，传入的参数data]，可以实现将获取的
            #body传输到下一个函数中去
            self.finished.callback(body)
        except Exception as e:
            print(e)


def cbRequest(response):
    print('Redirect Response code:', response.code)
    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)
    finished = defer.Deferred()
    response.deliverBody(BeginningPrinter(finished))
    finished.addCallback(lambda _:print(_))
    return finished


host= "211.147.239.101"
port = 44370
proxy_config = (host,port,"")




contextFactory = ScrapyClientContextFactory()

agent = TunnelingAgent(reactor,proxy_config,contextFactory,10,None,None)

d = agent.request(b'GET',b'https://www.baidu.com')
d.addCallback(cbRequest)
d.addErrback(lambda _:print(_))
d.addCallback(lambda _:print(time.clock()))
d.addBoth(lambda _:reactor.stop())
reactor.run()