from urllib.parse import urlparse,urlsplit,urlunparse

url = 'https://sh.lianjia.com/ershoufang/pudong/'

_url = url.strip()
print(_url)
parsed = urlparse(url)
print(parsed.scheme)
print(parsed.netloc)
print(parsed)
print(parsed)