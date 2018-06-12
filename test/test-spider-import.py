from importlib import import_module
from pkgutil import iter_modules
import sys,os

def import_spider(path):

    spiders = list()

    spider = import_module(path)
    spiders.append(spider)

    if hasattr(spider,"__path__"):
        print(spider.__path__)

        for _, subpath, ispkg in iter_modules(spider.__path__):
            # 取得模块的绝对路径
            fullpath = path + "." + subpath

            # 判断是模块包还是模块
            if ispkg:
                # 是模块包的话重新调用本方法将模块包下的所以模块都导入
                spiders += import_spider(fullpath)
            else:
                # 是模块的话就直接导入到结果中
                submod = import_module(fullpath)
                spiders.append(submod)
    else:
        print("no __path__")
    return spiders


s = import_spider("spider")
print(s)