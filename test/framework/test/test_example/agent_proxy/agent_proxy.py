import base64
import re
from pprint import pformat

from lxml import etree
from twisted.internet.ssl import ClientContextFactory
from twisted.python.log import err
from twisted.web.client import ProxyAgent, readBody
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint,SSL4ClientEndpoint
from twisted.web.http_headers import Headers


def display(response,url):
    print("Received response: %s"%url)
    print(response)
class WebClientContextFactory(ClientContextFactory):
    '''
    用来实现https网页的访问验证
    '''
    def getContext(self,hostname, port):
        return ClientContextFactory.getContext(self)

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

    print('Response version:', response.version)
    print('Response headers:')
    print(pformat(list(response.headers.getAllRawHeaders())))
    print('Response code:', response.code)
    print('Response phrase:', response.phrase)


    # d = readBody(response)
    # d.addCallback(get_onePage)
    # return d
host_01 = "149.28.192.96"
host = '47.105.165.81'
port = 5527
# header = Headers()
user_name = base64.b64encode('spider:123456'.encode('utf_8'))
encode_user = 'Basic '+str(user_name,'utf-8')
decode_user = base64.b64decode(user_name)
print(encode_user)
print(decode_user)
# header.addRawHeader('Proxy-Authenticate',user_name)
# def main():
endpoint = TCP4ClientEndpoint(reactor, host, port)
agent = ProxyAgent(endpoint)
d = agent.request(b"GET", b"https://sh.lianjia.com/xiaoqu/anshan",  Headers({'Proxy-Authenticate': [decode_user]}),)
d.addCallback(cbRequest)
d.addErrback(err)
d.addCallback(lambda ignored: reactor.stop())
reactor.run()
#
# if __name__ == "__main__":
#     main()