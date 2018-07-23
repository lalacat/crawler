

def arglist_to_dict(arglist):
    """
    将"key=value"转变成是"key:value"
    :param arglist:["key=value"]列表,传入参数的类型必须是list
    :return: 返回一个dict
    """
    return dict(x.split('=',1).strip() for x in arglist)