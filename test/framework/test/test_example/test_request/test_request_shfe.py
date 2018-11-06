import json
import jsonpath
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
url = "http://www.shfe.com.cn/data/dailydata/kx/pm20181008.dat"

# time = re.findall('\d{4}\d{1,2}\d{1,2}', url)
time = re.findall('.^201810\d{4}', url)

print(time)
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


# for oneitem in allitems:
#     if oneitem['PARTICIPANTABBR1'].strip() == '华泰期货':
#         # 持仓量
#         volume = oneitem['CJ1']
#         # print(volume)
#         # 排名
#         rank = oneitem['RANK']
#         # print(rank)
#         # 合约
#         instrumen = oneitem['INSTRUMENTID'].strip()
#         if re.match(instrumen_cu,instrumen):
#             print('true')
#         # print(instrumen)
#
#         print(instrumen+':\t'+str(rank)+':\t'+str(volume))