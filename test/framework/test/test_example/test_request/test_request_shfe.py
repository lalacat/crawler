import json
import pprint
import jsonpath
import time
from urllib.parse import urlparse, urlunparse, urljoin

import requests
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
express = "$.o_cursor[?(@[*].PARTICIPANTABBR1 =~ /'华泰期货.*' )]"
# express_01 = "$.o_cursor[*]" \
#              "[" \
#              "?(@.CJ3 = 277743)" \
#              "]"
express_01 = '$..o_cursor[*][PARTICIPANTABBR1]'
company = jsonpath.jsonpath(data,express_01)
print(company)