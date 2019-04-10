"""
用request登录美团

"""
import requests

cookies={
    'has_recent_activity': '1',
    '_octo': 'GH1.1.1477592343.1531820067',
    'logged_in': 'no',
    '_gh_sess': 'UEZzYnVCMVlhNkVOdE5rU1hWRFpDbmFlY0UyQ1Y2b3Z4TGw2NFlTMmJLUWk5VENVQ3Q4TWxiSWN5ckEyZXN0MUFkT29XVjQvbWJVbm9RV0JNQmc1TmU0UnBtK0taUXJpcElqUk5PNGZ5TjZOQ2ZPRVR4NU5WQXcrb2xWRnRBMnRPMkRWYzYvWmVGY0FrYU12Q3BVVTY3dXVSblliNG4rWjc2QXVwR2pjQ1pzZXM1MFk1MjU5OUw2WkFLTU1BMzJDWGlTeXliNzNaejlUaW43cWhFNzQ0MFFVVmJ1aEppbzdtQTZkRERmUm5mWExkRDlmWW5lNk9mdlFYb05MQUtubDZBbXFJWjV6eFhic3JiWlRtZ2QxZ2FqZUxnOGFheUgzaXJmc290b0Jma09pRTJZdHZySEVmdVdGZHVBU3ZTVTJRM0pESnE1N1VPRDM0ck9FZzNJZTN5VWljUktyZ3FZQU16THVBeFBXV3BNPS0tSDh4WVV6U2RSNjlBL3FNQ3VaRGxEUT09--71cf0886128d55b42c82cf6f7b76e007ebfdc77b',
    '_ga': 'GA1.2.57857743.1531820085',
    '_gat': '1',
    'tz': 'Asia%2FShanghai',

}

mt_cookies = {
'_mta':'211246762.1551792317872.1551792317872.1551792688339.2',
'uuid':'2dee62f074c04c1cab92.1551792314.1.0.0',
'SERV':'www',
'LREF':'aHR0cDovL3d3dy5tZWl0dWFuLmNvbS9hY2NvdW50L3NldHRva2VuP2NvbnRpbnVlPWh0dHBzJTNBJTJGJTJGd3d3Lm1laXR1YW4uY29tJTJGbWVpc2hpJTJGNTI2NzI1JTJG',
'passport.sid':'yzg4AjOd2rUr_X5RLHPKqujJHjbJ0l1t',
'passport.sid.sig':'XXs4m9KWsAdSNDUc9QOexgxXOus',
'mtcdn':'K'
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'passport.meituan.com',
    'Origin':'https://passport.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
# TODO
# 解决_token,fingerprint，csrf
data ={


}