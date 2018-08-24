from collections import defaultdict
import logging


class Scraper(object):
    pass

class MiddlewareManager(object):
    """
    中间件的父类
    """
    component_name = 'father middleware'

    def __init__(self,*middlewares):
        self.middlewares = middlewares
        self.methods = defaultdict(list)
        for mw in middlewares:
            self.__add_middlewares(mw)

    @classmethod
    #  子类实现该方法，从settings中获得方法，如果子类没呀重写该方法
    #  会报错
    def _get_mwlist_from_settings(cls,settings,crawler=None):
        raise NotImplementedError

    @classmethod
    def from_settings(cls,settings,crawler=None):
        """
        从default settings中加载默认的中间件
        :param settings:
        :param crawler:
        :return:
        """
        mwlist = cls._get_mwlist_from_settings(settings)
        middlewares = []
        enable = []
        for clspath in mwlist:
            pass