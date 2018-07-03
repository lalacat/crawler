
from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue,DeferredList
#from test.public_api.web import get_need_datas,print_result
import json,time
from bs4 import BeautifulSoup
from twisted.protocols.sip import URL
from twisted.python.urlpath import  URLPath
headers = {'User-Agent' :'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
            ,'content-type':"application/json"}
from six.moves.urllib.parse import (urljoin, urlsplit, urlunsplit,
                                    urldefrag, urlencode, urlparse,
                                    quote, parse_qs, parse_qsl,
                                    ParseResult, unquote, urlunparse)
from w3lib.util import to_bytes, to_native_str, to_unicode
import string
from urllib.parse import quote

# constants from RFC 3986, Section 2.2 and 2.3
RFC3986_GEN_DELIMS = b':/?#[]@'
RFC3986_SUB_DELIMS = b"!$&'()*+,;="
RFC3986_RESERVED = RFC3986_GEN_DELIMS + RFC3986_SUB_DELIMS
RFC3986_UNRESERVED = (string.ascii_letters + string.digits + "-._~").encode('ascii')
EXTRA_SAFE_CHARS = b'|'  # see https://github.com/scrapy/w3lib/pull/25
_safe_chars = RFC3986_RESERVED + RFC3986_UNRESERVED + EXTRA_SAFE_CHARS + b'%'

def safe_url_string(url, encoding='utf8', path_encoding='utf8'):
    """Convert the given URL into a legal URL by escaping unsafe characters
    according to RFC-3986.

    If a bytes URL is given, it is first converted to `str` using the given
    encoding (which defaults to 'utf-8'). 'utf-8' encoding is used for
    URL path component (unless overriden by path_encoding), and given
    encoding is used for query string or form data.
    When passing an encoding, you should use the encoding of the
    original page (the page from which the URL was extracted from).

    Calling this function on an already "safe" URL will return the URL
    unmodified.

    Always returns a native `str` (bytes in Python2, unicode in Python3).
    """
    # Python3's urlsplit() chokes on bytes input with non-ASCII chars,
    # so let's decode (to Unicode) using page encoding:
    #   - it is assumed that a raw bytes input comes from a document
    #     encoded with the supplied encoding (or UTF8 by default)
    #   - if the supplied (or default) encoding chokes,
    #     percent-encode offending bytes
    parts = urlsplit(to_unicode(url, encoding=encoding,
                                errors='percentencode'))

    # IDNA encoding can fail for too long labels (>63 characters)
    # or missing labels (e.g. http://.example.com)
    try:
        netloc = parts.netloc.encode('idna')
    except UnicodeError:
        netloc = parts.netloc

    # quote() in Python2 return type follows input type;
    # quote() in Python3 always returns Unicode (native str)
    return urlunsplit((
        to_native_str(parts.scheme),
        to_native_str(netloc).rstrip(':'),

        # default encoding for path component SHOULD be UTF-8
        quote(to_bytes(parts.path, path_encoding), _safe_chars),

        # encoding of query and fragment follows page encoding
        # or form-charset (if known and passed)
        quote(to_bytes(parts.query, encoding), _safe_chars),
        quote(to_bytes(parts.fragment, encoding), _safe_chars),
    ))
def print_qyl163_content(lis,u):
    urls = list()
    print("print:%s"%u)
    for l in lis:
        result = dict()
        try:
            href_temp = l.a.get("href")
            result["href"] = "http://www.qyl63.com" + href_temp
            result["title"] = l.a.get("title")
            result["img"] = l.a.div.img.get("src")
            u = result["href"]
            #解决url中带有中文字符
            #_us = safe_url_string(u)
            _us = quote(u).replace("%3A",":")
            child_web = getPage(_us.encode("utf-8"))
            #child_web = getPage(b"http://httpbin.org/get")
            child_web.addCallback(add_video_url,result)
            child_web.addCallback(print_dic)
            urls.append(child_web)
        except Exception as e :
            print(e)
    return DeferredList(urls)

def add_video_url(child_page,result):
    try:
        bs_obj = BeautifulSoup(child_page, "html.parser")
        video_url = bs_obj.find('div', id='player-container').video.source.get("src")
        result["video_url"] = video_url
    except Exception as e :
        print(e)
    return result


def get_qyl163_content(content):
    print("parse")
    try:
        bs_obj = BeautifulSoup(content,"html.parser")
        ul = bs_obj.find("ul","videos")
        lis = ul.find_all("li")

    except Exception as e :
        print(e)

    return lis



def print_dic(context):
    print("print_web")
    print(context)


def finish(context):
    print("finish")
    return None


@inlineCallbacks
def read_url(url):
    d = getPage(url.encode('utf-8'))
    try:
        d.addCallbacks(get_qyl163_content)
        d.addCallback(print_qyl163_content,url)
        d.addCallback(finish)
    except Exception as e :
        print(e)


    yield d



if __name__ == '__main__':
    start = time.clock()
    url = "http://www.qyl63.com/recent/"


    t1 = time.time()
    result = list()
    for i in range(2,5):
        i = str(i)
        u = url + i
        print(u)
        d = read_url(u)
        result.append(d)

    
    dd = defer.DeferredList(result)
    dd.addBoth(lambda _:reactor.stop())



    reactor.run()
    end =time.clock()
    print("运行时间%3.2f"%(end-start))