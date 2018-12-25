import json
import time
import re
import logging

from lxml import etree
from spider import Spider
from test.framework.https.request import Request

logger = logging.getLogger(__name__)


class CollectSold(Spider):
    """
    将所有小区的地址都写入数据库中
    """

    def __init__(self):
        self.name = ""
        self._start_urls = []
        self.total_number_community = 0
        self.result = dict()
        self.result_len = 0

        self.sold_db = False
        self.change_header = True
        self.change_proxy = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, info):
        base_name = "Task_"
        self._name = base_name+info

    @property
    def start_urls(self):
        return self._start_urls

    @start_urls.setter
    def start_urls(self,urls):
        if not isinstance(urls,list):
            self._start_urls = [urls]
        else:
            self._start_urls = urls

    def start_requests(self):
        yield Request(self.start_urls[0],callback=self._parse_sold)

    def _parse_sold(self,response):
        selector = etree.HTML(response.body)

        try:
            sold_houses = self._xpath_filter(selector.xpath("//ul[@class='listContent']")).xpath('./li')
            total_num = selector.xpath('//div[@class="total fl"]/span/text()')[0]

            if int(total_num) == 0:
                return self._reload_sold(response,sold_houses)
            else:
                self._resolve_sold(sold_houses,response.url)
                if int(total_num) > len(sold_houses):

                    if not re.search('pg',response.url):
                        print("sold：" + self.name + ': ' + response.url + ': ' + str(total_num) + "===" + str(len(sold_houses)))
                        page_number = selector.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
                        total_page_number = json.loads(page_number[0])["totalPage"]
                        base_name = response.url.split('/')[-2]
                        for pg in range(2,total_page_number+1):
                            url = response.url.replace(base_name,'pg'+str(pg)+base_name)
                            yield Request(url, callback=self._parse_sold)
                    else:
                        pg = re.findall('pg\d+',response.url)[0]
                        print("sold：" + self.name + '_' + pg + ': ' + response.url + ': ' + str(total_num) + "===" + str(len(sold_houses)))
                        return None
        except Exception as e:
            logger.error(*self.lfm.error(
                'Spider', self.name,
                '解析房子信息时出现错误',
                {
                    'request':response.request,
                    'function':'total_num={0} sold_houses={1}'.format(int(total_num),len(sold_houses))
                }),
                extra={
                    'exception':e,
                    'time':time.clock()
                }
                )
            return None

    def _reload_sold(self,response,sold_houses):
        if response.request.meta.get('download_times'):
            download_times = response.request.meta['download_times']
            logger.critical(*self.lfm.crawled(
                'Spider', self.name,
                '({0})再次下载,时间为：'.format(response.request.headers.getRawHeaders('User-Agent')[0]),
                {
                    'function': '第{0}次'.format(download_times),
                    'request': response.request,
                    'time':time.clock(),
                }
            ))
            download_times = download_times + 1
        else:
            download_times = 1

        if download_times < 4:
            return Request(response.url, callback=self._parse_sold, meta={
                'download_times': download_times,
                'header_flag': True,
                'last_header': response.request.headers
            })
        else:
            logger.critical(*self.lfm.crawled(
                'Spider', self.name,
                '重复下载次数已超过最大值，判断此网页没有数据,时间为：',
                {
                    'function': '第{0}次'.format(download_times),
                    'request': response.request,
                    'time':time.clock(),
                }
            ))
            logger.error(response.url,extra={
                'exception':'重复下载次数已超过最大值，判断此网页没有数据',
                'time':time.clock(),
                'reason':'No Data',
                'recordErrorUrl':True
            })
            print("sold：" + self.name + ': ' + response.url + ': ' + str(0) + "===" + str(len(sold_houses)))
            return None

    def _resolve_sold(self,sold_houses,url):
        base_xpath = './div[@class="info"]'

        for sold_house in sold_houses:
            house_info = dict()
            sold_title = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="title"]/a/text()'))
            # print("小区名称："+sold_title)
            # solf_title_key = sold_title.replace('.','_')
            # house_info['sold_title'] = sold_title

            sold_address = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="houseInfo"]/text()'))
            # print("小区地址："+sold_address)
            house_info['sold_address'] = sold_address

            sold_dealDate = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="dealDate"]/text()'))
            # print("成交日期："+sold_dealDate)
            house_info['sold_dealDate'] = sold_dealDate

            sold_house_url = self._xpath_filter(sold_house.xpath('./a/@href'))
            house_info['sold_house_url'] = sold_house_url

            sold_totalPrice = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="address"]/div[@class="totalPrice"]/span/text()'))
            # print("成交价格："+sold_totalPrice)
            house_info['sold_totalPrice'] = sold_totalPrice
            if re.search('\*+',sold_totalPrice):
                # 记录错误呀的URL
                logger.error(sold_house_url,extra={
                    'reason':'价格隐藏',
                    'exception':sold_title,
                    'time':time.clock(),
                    'recordErrUrl':True
                })



            sold_unitPrice = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="unitPrice"]/span/text()'))
            # print('成交均价：'+sold_unitPrice)
            house_info['sold_unitPrice'] = sold_unitPrice

            sold_positionInfo = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="flood"]/div[@class="positionInfo"]/text()'))
            # print("楼层高度："+sold_positionInfo)
            house_info['sold_positionInfo'] = sold_positionInfo


            sold_saleonborad = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]/text()'))
            # print("挂牌价："+sold_saleonborad)
            house_info['sold_saleonborad'] = sold_saleonborad

            sold_dealcycle = \
            self._xpath_filter(sold_house.xpath(base_xpath + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]/text()'))
            # print("成交周期："+sold_dealcycle)
            house_info['sold_dealcycle'] = sold_dealcycle
            self.result[(sold_title+'('+sold_totalPrice+')').replace('.','_')] = house_info

    def _xpath_filter(self,xpath):
        if xpath:
            return xpath[0]
        else:
            return ' '





# url = 'https://sh.lianjia.com/chengjiao/c5011000013330/'
# url_01 ='https://sh.lianjia.com/chengjiao/c5011000013330/'
# name = url_01.split('/')[-2]
# # print(name)
# url_02 = url_01.replace(name,'pg2'+name)
# # print(url_02)
# url_03 = re.search('pg',url_01)
# if url_03:
#     print(url_03)
# url_04 = re.findall('pg\d+',url_02)
# if url_04:
#     print(url_04)
