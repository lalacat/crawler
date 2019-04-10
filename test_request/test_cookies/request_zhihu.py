import requests

cookies = {

    "__utma":'51854390.1811439610.1539068036.1554103916.1554286112.70',
    "__utmc":'51854390',
    '__utmv':'51854390.100-1|2=registration_date=20110904=1^3=entry_date=20110904=1',
    '__utmz':'51854390.1554286112.70.69.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/318445847',
    '_xsrf':'6x7esFLcljRjnU4HlqpyC2i2qix4C3Yp',
    '_zap':'8faa3e3b-5a44-4633-bea0-23110a2bd920',
    'capsion_ticket':"2|1:0|10:1554778076|14:capsion_ticket|44:ZTlkOGMwNDYzYWYyNDRmYmFhODUxZTk0MDMzOWVkMjg=|c9f1446c14dad9ac3602c8678ccd0570617b08b0b4c6841c587dc68e295ee628",
    'd_c0'	:'"AODmXnMaUw6PTmcaftH6VZVnsXydAqVAZPU=|1538875138"',
    'q_c1'	:'995684cfc1144a19be585900048195fc|1552885073000|1538985095000',
    'tgw_l7_route':'66cb16bc7f45da64562a077714739c11',
    'tst':	'r',
    'z_c0':	"2|1:0|10:1554778080|4:z_c0|92:Mi4xeDUwQkFBQUFBQUFBNE9aZWN4cFREaVlBQUFCZ0FsVk40RldaWFFDRnlKSDNfaS1PR1hqX3pOeGQ2ZlpZZ1hQV2Z3|a4382e99c964076fd9c8bfc3c2baacd91366aae5c0ed8cf8ba9d045e2d54aa89"
}

url = 'https://www.zhihu.com/follow'

headers = {
    'Connection': "keep-alive",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # 'Accept-Encoding': "gzip, deflate, br",
    # 'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    'content-type':"application/json",
}
r = requests.get(url, headers=headers)
r.encoding = "utf-8"
print(r.text)