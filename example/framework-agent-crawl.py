from twisted.web.client import getPage
from twisted.internet import reactor,defer
from twisted.internet.defer import inlineCallbacks,Deferred,returnValue
from test.public_api.web import get_need_datas,print_result
import json,time

class Requset(object):
    def __init__(self):
        pass