import warnings
from collections import defaultdict
'''
使用到了list的解析；最多进行两次循环套接
join()；针对是一个列表数据处理，即join("a","b","c")是将这几个字符串连起来
format（）；


'''

def _check_name_duplicates(_found):
    dupes = ["\n".join("  {cls} named {name!r} (in {module})".format(
        module=lis[0], cls=lis[1], name=name)
                       for lis in locations)
             for name, locations in _found.items()
             if len(locations) > 1]
    if dupes:
        msg = ("\nThere are several spiders with the same name:\n\n"
               "{}\n\n  This can cause unexpected behavior.".format(
            "\n\n".join(dupes)))
        warnings.warn(msg, UserWarning)


found1 ={'task1': ('spider.spider1', 'Spider1'),
        'task2': ('spider.spider2', 'Spider2'),
        'task3': ('spider.spider3', 'Spider3'),
        'task4': ('spider.spider4', 'Spider4'),
        'task5': ('spider.spider5', 'Spider5'),
        'task6': ('spider.spider6', 'Spider6'),
        'task7': ('spider.spider7', 'Spider7'),
        'task8': ('spider.spider8', 'Spider8'),
        'task9': ('spider.spider9', 'Spider9')}
found2 = {
    'task1': ('spider.spider10', 'Spider10'),
    'task7': ('spider.spider17', 'Spider17'),
    'task7': ('spider.spider37', 'Spider37')

}
_found = defaultdict(list)
for k,v in found1.items():
    _found[k].append(v)

for k,v in found2.items():
    _found[k].append(v)

_check_name_duplicates(_found)

