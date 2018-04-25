import urllib
import requests
import json

headers = { 'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}


value = {'key1':"value1","key2":"value2"}
files = {"file":open("ghostdriver.log",'rb')}
cookies = dict(cookies_are = "working")

s = requests.session()
s.get('https://httpbin.org/cookies/set/sessioncookie/1234567')
s.headers.update(headers)
r = s.get('https://httpbin.org/headers')
#r = requests.get("https://httpbin.org/cookies",cookies=cookies)

print(r.url)
print(r.text)

"""
print(r.status_code)
print(r.encoding)
print(r.cookies)
"""