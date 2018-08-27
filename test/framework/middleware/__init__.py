from collections import defaultdict
import logging
import pprint

from test.framework.setting import Setting
from test.framework.objectimport.loadobject import load_object

logger = logging.getLogger(__name__)


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
        ls = list(settings["TEST"])
        return ls
        #raise NotImplementedError

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
        enabled = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                #  两个if用来判断mwcls是类的情况下，是跟crawler关联还是和settings相关联
                if crawler and hasattr(mwcls,'from_crawler'):
                    mw = mwcls.from_crawler(crawler)
                elif hasattr(mwcls,'from_settings'):
                    mw = mwcls.from_settings(settings)
                else:
                #  当mwcls不是类的时候，那就是方法
                    mw = mwcls()
                middlewares.appand(mw)
                enabled.append(clspath)
            except Exception as e :
                if e.args:
                    clsname = clspath.split('.')[-1]
                    logger.warning("Disabled %(clsname)s: %(eargs)s",
                                   {'clsname': clsname, 'eargs': e.args[0]},
                                   extra={'crawler': crawler})


        logger.info("Enabled %(componentname)ss:\n%(enabledlist)s",
                    {'componentname': cls.component_name,
                     'enabledlist': pprint.pformat(enabled)},
                    extra={'crawler': crawler})


    @classmethod
    def from_craweler(cls,crawler):
        return cls.from_settings(crawler.settings,crawler)


s = Setting()
m = MiddlewareManager.from_settings(s)