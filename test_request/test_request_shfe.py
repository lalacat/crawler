import json
import pprint

import jsonpath
import re
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "http://www.shfe.com.cn/data/dailydata/kx/pm20181008.dat"

r = requests.get(url,headers=header)
r.encoding = "utf-8"


data = json.loads(r.text)
# print(pprint.pformat(data))
# company = jsonpath.jsonpath(data,'$..o_cursor[?(@.PARTICIPANTABBR1=~/华泰期货.*/i)]')
# express = "$.o_cursor[?(@[*].PARTICIPANTABBR1 =~ /'华泰期货.*' )]"
# express_01 = "$.o_cursor[*]" \
#              "[" \
#              "?(@.CJ3 = 277743)" \
#              "]"
# express_01 = '$..o_cursor[*][PARTICIPANTABBR1]'
express = '$.o_cursor[*]'
allitems = jsonpath.jsonpath(data,express)
instrumen_cu  = 'cu\d+'
result = defaultdict(list)

instrumen_al  = 'al\d+'
instrumen_zn  = 'zn\d+'
instrumen_pb  = 'pb\d+'
instrumen_ni  = 'ni\d+'
instrumen_sn  = 'sn\d+'
instrumen_au  = 'au\d+'
instrumen_ag  = 'ag\d+'
instrumen_rb  = 'rb\d+'
instrumen_hc  = 'hc\d+'
instrumen_fu  = 'fu\d+'
instrumen_bu  = 'bu\d+'
instrumen_ru  = 'ru\d+'

b = lambda x:x.split('\\')[0]
# a = b(instrumen_cu)
total = 0
# print(a)
for oneitem in allitems:
    if oneitem['PARTICIPANTABBR1'].strip() == '华泰期货':
        # 持仓量
        volume = oneitem['CJ1'] if oneitem['CJ1'] else 0
        # print(volume)
        # 排名
        rank = oneitem['RANK']
        # print(rank)
        # 合约
        instrumen = oneitem['INSTRUMENTID'].strip()
        if re.match(instrumen_cu, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_cu)].append(result_temp)
            total += volume


        if re.match(instrumen_al, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_al)].append(result_temp)

        if re.match(instrumen_zn, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_zn)].append(result_temp)

        if re.match(instrumen_pb, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_pb)].append(result_temp)

        if re.match(instrumen_ni, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_ni)].append(result_temp)

        if re.match(instrumen_sn, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_sn)].append(result_temp)

        if re.match(instrumen_au, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_au)].append(result_temp)

        if re.match(instrumen_ag, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_ag)].append(result_temp
                                           )
        if re.match(instrumen_hc, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_hc)].append(result_temp)

        if re.match(instrumen_fu, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_fu)].append(result_temp)

        if re.match(instrumen_bu, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_bu)].append(result_temp)

        if re.match(instrumen_ru, instrumen):
            result_temp = instrumen + ':' + str(rank) + ':' + str(volume)
            result[b(instrumen_ru)].append(result_temp)

a = dict()
a['1'] = result
print(pprint.pformat(a))
print(total)
# print(a)