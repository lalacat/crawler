from test.framework.setting import BaseSettings, Setting
from operator import itemgetter
import logging,pprint
import numbers
logger = logging.getLogger(__name__)


def bulid_component_list(complist):

    if complist is None:
        raise ValueError("设置的参数有误，不能查找到")
    if isinstance(complist,dict):
        logger.info("载入的模块是dict类型，将按设置的优先级载入")
        #  operator.itemgetter函数获取的不是值，而是定义了一个函数，通过该函数作用到对象上才能获取值。
        for k,v in complist.items():
            if v is not None and not isinstance(v,numbers.Real):
                raise ValueError('模块 {} 存在无效值 {},请为模块提供一个确定的数值 '.format(k,v))
        comlist = [k for k ,v in sorted(complist.items(),key=itemgetter(1))]

    elif isinstance(complist,list):
        logger.info("载入的模块是list类型，将按设置的默认顺序载入")
        comlist = complist
    else:
        raise ValueError("设置的格式有误，将添加的class或fun，设置为："
                         "compoent_name = {class or fun : number} 或者"
                          "compoent_name = [class1,class2]")

    if len(comlist) != len(complist):
        raise ImportError("载入不完整缺少，存在模块没有导入")

    return comlist

s = Setting()
a = {"a":10,"b":20,"c":30,"d":5}

b = bulid_component_list(a)
for k in b :
    print(k)
c = [(1,2,3,4,5,6,7),(1,5,4,3,5,6,7),(1,7,8,3,5,6,2)]
b = itemgetter(1)
for i in c:
    for j in sorted(i,itemgetter(1)):
        print(j)
