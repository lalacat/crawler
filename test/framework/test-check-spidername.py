import warnings
from collections import defaultdict
def _check_name_duplicates(_found):
    dupes = ["\n".join("  {cls} named {name!r} (in {module})".format(
        module=mod, cls=cls, name=name)
                       for (mod, cls) in locations)
             for name, locations in _found.items()
             if len(locations) > 1]
    if dupes:
        msg = ("There are several spiders with the same name:\n\n"
               "{}\n\n  This can cause unexpected behavior.".format(
            "\n\n".join(dupes)))
        warnings.warn(msg, UserWarning)

students = {"a":"bob","b":"lili","c":'lala'}

print((type(students)))
for num,name in students.items():
    print(num,name)

found ={'task1': [('spider.spider10', 'Spider10')],
        'task1': [('spider.spider10', 'Spider10')],
        'task2': [('spider.spider2', 'Spider2')],
        'task3': [('spider.spider3', 'Spider3')],
        'task4': [('spider.spider4', 'Spider4')],
        'task5': [('spider.spider5', 'Spider5')],
        'task6': [('spider.spider6', 'Spider6')],
        'task7': [('spider.spider7', 'Spider7')],
        'task7': [('spider.spider7', 'Spider7')],
        'task7': [('spider.spider7', 'Spider7')],
        'task8': [('spider.spider8', 'Spider8')],
        'task9': [('spider.spider9', 'Spider9')]}
print(len(found))
_found = defaultdict(list)
i = 0
for k,v in found.items():

    print(len(v))
    _found[k].append(v)
    i += 1
print(i)
print(_found)
dupes = ["\n".join("  {cls} named  (in {module})".format(module=mod, cls=cls)
                   for (mod, cls) in students.items())]
put_data = ["\n".join(" {a} named {c!r} in {b}".format(a=num,b=name,c=m)
                for (num,name)in location) for m,location in found.items() ]

for i in put_data:
    pass
    #print(i)