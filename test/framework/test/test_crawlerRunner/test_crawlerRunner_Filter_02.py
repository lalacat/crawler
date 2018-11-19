import pprint
import queue

from collections import Iterable

import pymongo


# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

#连接到数据库myDatabase
DATABASE = "LianJia"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "XiaoQu"

xiaoqu = db[COLLECTION].find({})
one = xiaoqu.next()

db_coll = db[COLLECTION]
searchRes = db_coll.find({},{'_id':False})


#  list
town_urls_list = [
    'https://sh.lianjia.com/xiaoqu/anshan/',# 157 156
    'https://sh.lianjia.com/xiaoqu/dongwaitan/',# 144 141
    'https://sh.lianjia.com/xiaoqu/huangxinggongyuan/',#159 159
    'https://sh.lianjia.com/xiaoqu/kongjianglu/',
    'https://sh.lianjia.com/xiaoqu/wujiaochang/',
    'https://sh.lianjia.com/xiaoqu/xinjiangwancheng/',
    'https://sh.lianjia.com/xiaoqu/zhoujiazuilu/',
    'https://sh.lianjia.com/xiaoqu/zhongyuan1/',
]

# 所有URL,在community_url下的，dict没有命名的
queryArgs = [
    {"total_zone_name":"putuo"},
    {"total_zone_name":"minhang"},
    {"total_zone_name":"xuhui"},
    {"total_zone_name":"baoshan"},
    {"total_zone_name":"yangpu"},
    {"total_zone_name":"songjiang"},
    {"total_zone_name":"changning"},
    {"total_zone_name":"pudong"},
    {"total_zone_name":"jiading"},
    {"total_zone_name":"zhabei"},
    {"total_zone_name":"fengxian"},
    {"total_zone_name":"jiangan"},
    {"total_zone_name":"hongkou"},
    {"total_zone_name":"qingpu"},
    {"total_zone_name":"huangpu"},
    ]

all_zone =[]
for query in queryArgs:
    search = db_coll.find(query,{'_id':False})
    while True:
        try:
            next_task = search.next()
            #  task_name = next_task["total_zone_name"][0]
            for name, url in next_task.items():
                if name != 'total_zone_name':
                    all_zone.append(url)
        except StopIteration:
            break

#



def make_generator(obj):
    if isinstance(obj,Iterable):
        try:
            it = iter(obj)
        except Exception as e :
            print(e)
        while True:
            try:
                yield it.__next__()
            except StopIteration:
                return "over"
                break
    else:
        print('False')






print(len(all_zone))
_task_schedule = queue.Queue()
_next_task = None
_tasks = make_generator(all_zone)
SPIDER_NAME_CHOICE = True
name_num = 0
task_finish = False
temp_dict = None


def _create_task():
    global task_finish
    global _next_task
    global _tasks
    global temp_dict
    try:
        while _task_schedule.qsize() <= 10:

            if _next_task is None:
                temp_dict = next(_tasks)
                _next_task = filter(temp_dict)
            if isinstance(_next_task, tuple):
                _task_schedule.put(_next_task)
                _next_task = None
            else:
                try:
                    temp = next(_next_task)
                    filter_data = filter((temp,temp_dict[temp]))
                    if filter_data:
                      _task_schedule.put(filter_data)
                except StopIteration:
                    _next_task = None
        print('10次')
        return
    except StopIteration:
        print('爬完了')
        task_finish = True
        return


def filter(task):
    global name_num
    global SPIDER_NAME_CHOICE

    if isinstance(task,str) and not SPIDER_NAME_CHOICE:
        raise ValueError('爬虫的URL需要设置名称，或者将{SPIDER_NAME_CHOICE}设置为True,使用默认值！')
    if SPIDER_NAME_CHOICE:

        name = str(name_num)
        name_num += 1
        if isinstance(task,str):
            url = task
        else:
            if not isinstance(task,dict):
                raise TypeError('task(%s)的类型必须是<str>或者包含关键字{%s}的<dict>，'
                                '或者将{SPIDER_NAME_CHOICE}设置为False，自动为每个task设置名称'
                                % (type(task), 'community_url'))
            else:
                if task.get('community_url'):
                    url = task['community_url']
                else:
                    raise KeyError('task(%s)包含关键字{%s}' % (type(task), 'community_url'))
    else:
        if isinstance(task, dict):
            if len(task) == 1:
                name = [key for key in task.keys()][0]
                url = [value for value in task.values()][0]
            elif len(task) > 1 :
                return make_generator(task)
            else:
                raise TypeError('task(%s)的类型必须是<dict>，或者将{SPIDER_NAME_CHOICE}设置为True，自动为每个task设置名称'%type(task))
        else:
            if isinstance(task, tuple):
                if task[0] == 'total_zone_name':
                    return None
                name = task[0]
                url = task[1]

    return (name, url)



def get_schedule():
    while True:
        try:
            temp = _task_schedule.get(block=False)
            print(temp)
        except queue.Empty:
            break


while not task_finish or _task_schedule.qsize() > 0:
    if _task_schedule.qsize()>0:
        get_schedule()
    else:
        _create_task()