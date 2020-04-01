import json
import re
from collections import defaultdict

import jsonpath

from test.framework.spider import Spider
import logging
from twisted.internet import reactor

from test.framework.core.crawler import Crawler
from test.framework.https.request import Request
from test.framework.setting import Setting
logger = logging.getLogger(__name__)

class SHFE_Rank(Spider):
    """
    将所有小区的地址都写入数据库中
    """
    name = "shfe"

    def __init__(self):

        self.total_cu = 0
        self.total_al = 0
        self.total_zn = 0
        self.total_pb = 0
        self.total_ni = 0
        # self.name = ['华泰','中信','东证','海通']
        self.instrument_cu = 'cu\d+'
        self.instrument_al = 'al\d+'
        self.instrument_zn = 'zn\d+'
        self.instrument_pb = 'pb\d+'
        self.instrument_ni = 'ni\d+'
        self.instrument_sn = 'sn\d+'
        self.instrument_au = 'au\d+'
        self.instrument_ag = 'ag\d+'
        self.instrument_rb = 'rb\d+'
        self.instrument_wr = 'wr\d+'
        self.instrument_ss = 'ss\d+'
        self.instrument_sc = 'sc\d+'
        self.instrument_hc = 'hc\d+'
        self.instrument_fu = 'fu\d+'
        self.instrument_bu = 'bu\d+'
        self.instrument_ru = 'ru\d+'
        self.instrument_nr = 'nr\d+'
        self.instrument_sp = 'sp\d+'

        self.total_result = dict()

    def start_requests(self):

        self.start_urls = [
        'http://www.shfe.com.cn/data/dailydata/kx/pm20190102.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190103.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190104.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190107.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190108.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190109.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190110.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190111.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190114.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190115.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190116.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190117.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190118.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190121.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190122.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190123.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190124.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190125.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190128.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190129.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190130.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190131.dat',

         'http://www.shfe.com.cn/data/dailydata/kx/pm20190201.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190211.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190212.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190213.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190214.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190215.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190218.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190219.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190220.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190221.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190222.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190225.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190226.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190227.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190228.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190301.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190304.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190305.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190306.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190307.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190308.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190311.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190312.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190313.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190314.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190315.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190318.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190319.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190320.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190321.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190322.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190325.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190326.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190327.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190328.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190329.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190401.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190402.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190403.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190404.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190408.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190409.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190410.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190411.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190412.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190415.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190416.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190417.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190418.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190419.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190422.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190423.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190424.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190425.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190426.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190429.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190430.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190506.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190507.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190508.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190509.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190510.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190513.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190514.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190515.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190516.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190517.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190520.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190521.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190522.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190523.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190524.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190527.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190528.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190529.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190530.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190531.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190603.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190604.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190605.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190606.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190610.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190611.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190612.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190613.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190614.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190617.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190618.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190619.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190620.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190621.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190624.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190625.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190626.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190627.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190628.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190701.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190702.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190703.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190704.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190705.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190708.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190709.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190710.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190711.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190712.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190715.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190716.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190717.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190718.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190719.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190722.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190723.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190724.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190725.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190726.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190729.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190730.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190731.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190801.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190802.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190805.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190806.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190807.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190808.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190809.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190812.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190813.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190814.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190815.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190816.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190819.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190820.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190821.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190822.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190823.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190826.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190827.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190828.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190829.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190830.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190902.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190903.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190904.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190905.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190906.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190909.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190910.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190911.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190912.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190916.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190917.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190918.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190919.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190920.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190923.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190924.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190925.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190926.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190927.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20190930.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191008.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191009.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191010.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191011.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191014.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191015.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191016.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191017.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191018.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191021.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191022.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191023.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191024.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191025.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191028.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191029.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191030.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191031.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191101.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191104.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191105.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191106.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191107.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191108.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191111.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191112.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191113.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191114.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191115.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191118.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191119.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191120.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191121.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191122.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191125.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191126.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191127.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191128.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191129.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191202.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191203.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191204.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191205.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191206.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191209.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191210.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191211.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191212.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191213.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191216.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191217.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191218.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191219.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191220.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191223.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191224.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191225.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191226.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191227.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191230.dat',
         'http://www.shfe.com.cn/data/dailydata/kx/pm20191231.dat'
        ]

        # self.start_urls = [
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191008.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191009.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191010.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191011.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191012.dat',
        #
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181015.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181016.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181017.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181018.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181019.dat',
        #
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181022.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181023.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181024.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181025.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181026.dat',
        #
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181029.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181030.dat',
        # 'http://www.shfe.com.cn/data/dailydata/kx/pm20181031.dat'

        # ]

        for url in self.start_urls:
            yield Request(url, callback=self._parse)

    def _parse(self,response):
        data = json.loads(response.body)
        time = re.findall('\d{4}\d{1,2}\d{1,2}',response.url)
        b = lambda x: x.split('\\')[0]

        # print(time)

        express = '$.o_cursor[*]'
        allitems = jsonpath.jsonpath(data, express)

        result = defaultdict(list)

        for oneitem in allitems:
            if oneitem['PARTICIPANTABBR1'].strip() == '海通期货':
                # 持仓量
                volume = oneitem['CJ1']
                # print(volume)
                # 排名
                rank = oneitem['RANK']
                # print(rank)
                # 合约
                instrument = oneitem['INSTRUMENTID'].strip()
                if re.match(self.instrument_cu, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_cu)].append(result_temp)

                if re.match(self.instrument_al, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_al)].append(result_temp)

                if re.match(self.instrument_zn, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_zn)].append(result_temp)

                if re.match(self.instrument_pb, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_pb)].append(result_temp)

                if re.match(self.instrument_ni, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_ni)].append(result_temp)

                if re.match(self.instrument_sn, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_sn)].append(result_temp)

                if re.match(self.instrument_au, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_au)].append(result_temp)

                if re.match(self.instrument_wr, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_wr)].append(result_temp)

                if re.match(self.instrument_ss, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_ss)].append(result_temp)

                if re.match(self.instrument_sc, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_sc)].append(result_temp)

                if re.match(self.instrument_ag, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_ag)].append(result_temp)

                if re.match(self.instrument_hc, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_hc)].append(result_temp)

                if re.match(self.instrument_fu, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_fu)].append(result_temp)

                if re.match(self.instrument_bu, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_bu)].append(result_temp)

                if re.match(self.instrument_ru, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_ru)].append(result_temp)

                if re.match(self.instrument_sp, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_sp)].append(result_temp)

                if re.match(self.instrument_nr, instrument):
                    result_temp = instrument + ':' + str(rank) + ':' + str(volume)
                    result[b(self.instrument_nr)].append(result_temp)



        self.total_result[time[0]] = result
        return None



if __name__ == '__main__':
    settings = Setting()
    crawler_01 = Crawler(SHFE_Rank, settings)
    c1 = crawler_01.crawl()
    c1.addBoth(lambda _: reactor.stop())
    reactor.run()
