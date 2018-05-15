import requests
import json
import time
header = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}

url = "https://www.smzdm.com/homepage/json_more?timesort=152626079422&p=2"
urls = ["https://www.smzdm.com/homepage/json_more?p=1",
        "https://www.smzdm.com/homepage/json_more?p=2",
        "https://www.smzdm.com/homepage/json_more?p=3",
        ]
for url in urls:
    r = requests.get(url,headers=header)
    r.encoding = "utf-8"
    result=r.json()
    #print(type(result))
    for k in result["data"][1]["article_title"]:
        pass
        #print(k)

t = time.localtime(152626079422)
print(t)