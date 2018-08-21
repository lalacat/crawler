from urllib.parse import urlparse,urlsplit,urlunparse


def to_bytes(text, encoding=None, errors='strict'):
    """用于将传入的text转换为bytes类型的数据"""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    try:
        result = text.encode(encoding, errors)
    except UnboundLocalError :
        result = text.encode("utf-8", errors)
    return result

def _parsed_url_agrs(parsed):
    """
    将分割后的url不同块进行byte化，返回 scheme, netloc, host, port, path
    :return:
    """
    # b是一个匿名函数s是变量，用于将字符串byte化
    b = lambda s: to_bytes(s,encoding='ascii')
    scheme = b(parsed.scheme)
    netloc = b(parsed.netloc)
    # 将urlparse分解的各个变量合成标准的url
    path = urlunparse(['','',parsed.path or '/',parsed.params,parsed.query,''])
    path = b(path)
    print(path)
    host = b(parsed.hostname)
    port = parsed.port
    if port is None:
        port = 443 if scheme == b'https' else 80
    return scheme, host, port, path

def _parsed(url):
    """
    将一个标准的URL链接格式：scheme://nrtlooc/path;paramters?query#fragment
    将url分割成scheme, netloc,path,params,query,fragment这几个参数
    :param url:
    :return:
    """
    url = url.strip()
    parsed = urlparse(url)
    return _parsed_url_agrs(parsed)

'''
url = "blob:https://10012580.10012580.com/3f877248-fd3f-4166-a3b4-d6e2ceee752d"
url2 = "https://www.cnblogs.com:8800/shuchao/"
parsed = _parsed(url)
print(parsed)
'''