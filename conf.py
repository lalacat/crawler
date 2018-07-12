

def arglist_to_dict(arglist):
    """
    将"key=value"转变成是"key:value"
    :param arglist:"key=value"列表
    :return: 返回一个dict
    """
    return dict(x.split('=',1) for x in arglist)