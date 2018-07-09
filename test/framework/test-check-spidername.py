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
        'task2': [('spider.spider2', 'Spider2')],
        'task3': [('spider.spider3', 'Spider3')],
        'task4': [('spider.spider4', 'Spider4')],
        'task5': [('spider.spider5', 'Spider5')],
        'task6': [('spider.spider6', 'Spider6')],
        'task7': [('spider.spider37', 'Spider37')],
        'task8': [('spider.spider8', 'Spider8')],
        'task9': [('spider.spider9', 'Spider9')]}
found2 = {
    'task1': [('spider.spider11', 'Spider11')],
    'task7': [('spider.spider7', 'Spider7')],
    'task7': [('spider.spider27', 'Spider27')],

}
_found = defaultdict(list)
i = 0
for k,v in found.items():

    #print(len(v))
    _found[k].append(v)
    i += 1

for k,v in found2.items():
    _found[k].append(v)

#print(_found)


'''
dupes = ["\n".join("  {cls} named {name!r} (in {module})".format(
    module=mod, cls=cls, name=name) 
                   for (mod, cls) in location for location in locations for name, locations in _found.items()
         if len(locations) )> 1]
'''

for name,locations in _found.items():
    #print(locations)
    if len(locations) > 1 :
        for (x) in locations :
            for(z,y) in x:
                #print(name,z,y)
                pass

temp = [("{a},{b},{c}".format(a=i,b=b,c=len(b)) for i in b) for a,b in _found.items()]
for i in temp:
    print(temp)
