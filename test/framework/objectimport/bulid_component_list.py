from operator import itemgetter
import logging
import numbers
import pprint
logger = logging.getLogger(__name__)


def bulid_component_list(complist,name):

    if complist is None:
        raise ValueError("%s设置的参数有误，不能查找到所要添加的中间件，重新检查配置名称！(来自bulid_component_list)"%name)
    if isinstance(complist,dict):
        logger.debug("%s 载入的中间件是<dict>类型，将按设置的优先级载入"%name)
        #  operator.itemgetter函数获取的不是值，而是定义了一个函数，通过该函数作用到对象上才能获取值。
        for k,v in complist.items():
            if v is not None and not isinstance(v,numbers.Real):
                raise ValueError('模块 {} 存在无效值 {},请为模块提供一个确定的数值 '.format(k,v))
        comlist = [k for k,v in sorted(complist.items(),key=itemgetter(1))]

    elif isinstance(complist,list):
        logger.debug("%s 载入的模块是<list>类型，将按设置的默认顺序载入"%name)
        comlist = complist
    else:
        raise ValueError("%s设置的格式有误，将添加的class或fun，设置为："
                         "compoent_name = {class or fun : number} 或者"
                          "compoent_name = [class1,class2]!(来自bulid_component_list)"%name)

    if len(comlist) != len(complist):
        raise ImportError("%s载入不完整缺少，存在模块没有导入!(来自bulid_component_list)"%name)

    return comlist
